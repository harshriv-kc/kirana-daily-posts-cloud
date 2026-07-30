#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_kirana.py — fetch the latest available व्यापार केसरी (VK) PDF for the
kirana daily-posts routine, and decide WHICH posting date this run is for.

DATE LOGIC (no rigid run_date+1 formula — decide logically):
  The posting date is ALWAYS the date the clock allows right now (STAY CURRENT);
  a run is due only while there is still something owed.

  1. last_posted = newest `date` recorded in the dedup ledger
                   (kirana-used-log.json -> runs[].date = posting_date).
  2. next_owed   = last_posted + 1 day   (the earliest day we still owe).
  3. max_allowed = the furthest date this run may target, based on IST clock:
        - run fires AT/AFTER 7:30 PM IST  -> max_allowed = today + 1  (evening = next-day run)
        - run fires BEFORE   7:30 PM IST  -> max_allowed = today      (same-day run / catch-up)
  4. posting_date:
        - if next_owed <= max_allowed -> posting_date = max_allowed  (stay current)
        - else                        -> NOTHING DUE (already caught up; too early for next day)

  Why NOT gap-fill (fixed 27-Jul-2026): backfilling the oldest owed date makes a
  single missed run permanent. The Sat 25-Jul-2026 evening run was missed, so the
  Sun 26-Jul run filled 26-Jul (same day) instead of 27-Jul — and every later
  evening run would have kept filling the stale owed date, leaving the routine
  exactly one day behind forever. Skipping the stale date(s) keeps it current;
  any skipped dates are reported in date_decision.skipped_owed_dates.
  To deliberately publish a missed day, run with --posting-date YYYY-MM-DD.

  Catch-up still works: a missed evening run that fires after midnight (e.g. 2 AM
  on the 28th) still produces the 28th, because before the cutoff max_allowed=today.

  Examples (cutoff 6:00 PM IST):
    - 28th 02:00, ledger last=27th -> next_owed=28, max=28 -> post 28  (catch-up for today)
    - 28th 19:30, ledger last=28th -> next_owed=29, max=29 -> post 29  (normal evening)
    - 28th 19:30, ledger last=26th -> next_owed=27, max=29 -> post 29  (skip stale 27; stay current)
    - 28th 14:00, ledger last=28th -> next_owed=29, max=28 -> NOTHING DUE (too early for 29)

PDF used = the LATEST AVAILABLE paper, searched backwards from (posting_date - 1).
This naturally handles weekends (Sunday has no VK edition -> fall back to the most
recent one). gap_days = posting_date - pdf_date_used; on a normal day == 1.

STALENESS GUARD (added after the 30-Jul-2026 near-miss): falling back is only safe
when the skipped day genuinely has no paper. On 29-Jul-2026 the paper existed but
was published as VK-29-JULY-2026-Binder.pdf, which no filename guess covered; the
fetcher fell back to the already-consumed 28-Jul paper and still reported ok=true
with weekend_fallback=true on a Wednesday. Two fixes:
  - the paper about to be served is cross-checked against the ledger, and a paper
    predating last_posted (i.e. one already mined for an earlier posting) is a hard
    failure: {"ok":false,"pdf_not_resolvable":true,"stale_pdf":true}, exit 4.
    Override deliberately with --allow-stale-pdf.
  - `weekend_fallback` now means what its name says (every skipped date is a Sunday).
    The raw "gap > 1" signal it used to carry moved to `older_paper_used`.

Posting itself is done by the existing poster (post_items.py) — NOT here.

Usage:
  python run_kirana.py fetch [--posting-date YYYY-MM-DD] [--max-back 4]
                             [--cutoff HH:MM] [--ledger PATH] [--allow-stale-pdf]
      Decides the posting date (unless --posting-date forces it), downloads the
      newest available VK PDF to ./pdfs/, and prints one JSON line:
        {"ok":true,"path":...,"url":...,"posting_date":"YYYY-MM-DD",
         "pdf_date_used":"YYYY-MM-DD","expected_pdf_date":"YYYY-MM-DD","gap_days":N,
         "weekend_fallback":bool,"older_paper_used":bool,"stale_pdf":false,
         "date_decision":{...},...}

  Exit codes:
      0  a usable, non-stale paper was downloaded
      2  no paper found at all within max-back days   (pdf_not_resolvable)
      3  nothing due yet — already caught up           (nothing_due)
      4  only a stale (already-used) paper was found   (pdf_not_resolvable + stale_pdf)
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone, time as dtime, date as ddate

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IST = timezone(timedelta(hours=5, minutes=30))
DEFAULT_LEDGER = os.path.join(BASE_DIR, "kirana-used-log.json")

# vyaparkesari.com filenames are named INCONSISTENTLY by whoever uploads them:
# the English month token varies in case day-to-day within the same folder, e.g.
#   VK-04-JULY-2026.pdf   (uppercase)   but   VK-06-July-2026.pdf   (title-case).
# There is no reliable rule, so we PROBE every variant per date and use whichever
# returns a real PDF, instead of guessing one filename (which silently 404'd and
# fell back to a stale older paper).
URL_TMPL = "https://vyaparkesari.com/palaheeh/{yyyy}/{mm}/VK-{dd}-{MONTH}-{yyyy}{SUF}.pdf"
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://vyaparkesari.com/"}
MIN_PDF_BYTES = 500_000  # a real VK PDF is multi-MB; guard against error pages

# Trailing-token variants observed in the media library. 29-Jul-2026 shipped as
# VK-29-JULY-2026-Binder.pdf, which every no-suffix guess missed — the fetcher then
# silently served the already-consumed 28-Jul paper and still reported ok=true.
# Ordered cheapest-first: the bare name covers most days, so the extra variants
# only cost probes on the days that actually need them.
FILENAME_SUFFIXES = ["", "-Binder", "-binder", "-BINDER", "-1", "-2"]

# The e-paper post body on the website is subscription-gated, so the real
# attachment URL cannot be scraped; probing the upload path is the only public
# route. Keep this list append-only as new naming quirks show up.


def _ist_now():
    return datetime.now(IST)


def _urls_for(d):
    """Candidate URLs for date d across every naming variation the site actually uses.
    Three independent inconsistencies, confirmed by auditing Jun-Jul 2026 filenames:
      - month-name CASE varies day to day: VK-04-JULY vs VK-06-July.
      - the day is sometimes zero-padded, sometimes not: VK-08-... vs VK-8-... .
      - some days carry a trailing token: VK-29-JULY-2026-Binder.pdf.
    So we probe {suffix} x {padded, unpadded} day x {UPPER, Title, lower} month and
    use whichever returns a real PDF. (No abbreviated month like 'Jul' was ever
    observed, so full month name only.) Suffix is the OUTER loop so all bare names
    are tried before any suffixed one. Dedup, order-preserving."""
    yyyy, mm = d.strftime("%Y"), d.strftime("%m")
    days = [d.strftime("%d"), str(d.day)]            # e.g. "08" and "8" (same for >=10)
    month = d.strftime("%B")                          # full English month, e.g. "July"
    months = [month.upper(), month.capitalize(), month.lower()]
    urls, seen = [], set()
    for suf in FILENAME_SUFFIXES:
        for day in days:
            for mon in months:
                u = URL_TMPL.format(yyyy=yyyy, mm=mm, dd=day, MONTH=mon, SUF=suf)
                if u not in seen:
                    seen.add(u)
                    urls.append(u)
    return urls


def _head_probe(url):
    """Cheap existence check before spending a multi-MB GET.
    Returns (True|False|None, note); None means 'inconclusive, go ahead and GET'.
    With ~36 candidates per date, probing with HEAD keeps a miss fast."""
    try:
        r = requests.head(url, headers=HEADERS, timeout=45, allow_redirects=True)
    except Exception as e:
        return None, f"HEAD {type(e).__name__}: {e}"
    if r.status_code in (403, 405, 501):
        return None, f"HEAD unsupported (HTTP {r.status_code})"
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}"
    ctype = r.headers.get("content-type", "").lower()
    try:
        clen = int(r.headers.get("content-length") or 0)
    except ValueError:
        clen = 0
    if "pdf" not in ctype and clen and clen < MIN_PDF_BYTES:
        return False, f"not a pdf (ctype={ctype}, len={clen})"
    if clen and clen < MIN_PDF_BYTES:
        return False, f"too small ({clen} bytes)"
    return None, "head-ok"


def _try_download(d):
    """Probe every naming variant for date d. Returns (ok, url, payload_or_errsummary, tried).
    `url` is the working URL on success (exact server filename), else the first tried.
    `tried` lists each attempt so callers can log exactly what was probed."""
    tried = []
    urls = _urls_for(d)
    for url in urls:
        exists, note = _head_probe(url)
        if exists is False:
            tried.append({"url": url, "result": note})
            continue
        try:
            r = requests.get(url, headers=HEADERS, timeout=120)
        except Exception as e:
            tried.append({"url": url, "result": f"{type(e).__name__}: {e}"})
            continue
        if r.status_code != 200:
            tried.append({"url": url, "result": f"HTTP {r.status_code}"})
            continue
        ctype = r.headers.get("content-type", "")
        if "pdf" not in ctype.lower() or len(r.content) < MIN_PDF_BYTES:
            tried.append({"url": url, "result": f"not a pdf (ctype={ctype}, bytes={len(r.content)})"})
            continue
        tried.append({"url": url, "result": "ok"})
        return True, url, r.content, tried
    summary = "; ".join(f"{t['url'].rsplit('/', 1)[-1]}={t['result']}" for t in tried)
    return False, urls[0], summary, tried


def _no_paper_gap(pdf_date, posting):
    """True only when EVERY date skipped between the paper used and the expected
    paper date is a Sunday — VK publishes Mon-Sat, so a Sunday hole is a genuine
    reason to fall back to an older paper.

    This is what `weekend_fallback` always claimed to mean. It previously carried
    the value of `gap_days > 1`, so a plain missing weekday paper (29-Jul-2026 was
    a Wednesday) reported weekend_fallback=true and read as sanctioned."""
    holes, d = [], pdf_date + timedelta(days=1)
    end = posting - timedelta(days=1)
    while d <= end:
        holes.append(d)
        d += timedelta(days=1)
    return bool(holes) and all(x.weekday() == 6 for x in holes)


def _last_posted_date(ledger_path):
    """Newest posting_date recorded in the dedup ledger, or None if unavailable."""
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    dates = []
    for run in data.get("runs", []):
        ds = run.get("date")
        if not ds:
            continue
        try:
            dates.append(datetime.strptime(ds, "%Y-%m-%d").date())
        except ValueError:
            continue
    return max(dates) if dates else None


def _parse_cutoff(s):
    hh, mm = s.split(":")
    return dtime(int(hh), int(mm))


def decide_posting_date(now_ist, cutoff, last_posted):
    """Return (posting_date_or_None, decision_dict). None => nothing due yet."""
    today = now_ist.date()
    after_cutoff = now_ist.time() >= cutoff
    max_allowed = today + timedelta(days=1) if after_cutoff else today

    if last_posted is None:
        # No history: just post the time-appropriate date (no gap to fill).
        posting = max_allowed
        reason = "no ledger history -> post the time-appropriate date"
    else:
        next_owed = last_posted + timedelta(days=1)
        if next_owed <= max_allowed:
            # STAY CURRENT: never target a date older than the time-appropriate
            # one. A missed run leaves a stale owed date behind; backfilling it
            # publishes yesterday's date today and keeps the routine exactly one
            # day behind forever. Skip the stale date(s) instead.
            # (To deliberately publish a missed day, use --posting-date.)
            posting = max_allowed
            reason = ("skipped stale owed date(s) to stay current"
                      if next_owed < max_allowed else "normal next-day/same-day run")
        else:
            posting = None
            reason = ("already caught up; next owed date is beyond what the "
                      "current time allows (before 7:30 PM = same day only)")

    decision = {
        "now_ist": now_ist.isoformat(timespec="seconds"),
        "cutoff_ist": cutoff.strftime("%H:%M"),
        "after_cutoff": after_cutoff,
        "today_ist": today.isoformat(),
        "max_allowed": max_allowed.isoformat(),
        "last_posted": last_posted.isoformat() if last_posted else None,
        "next_owed": (last_posted + timedelta(days=1)).isoformat() if last_posted else None,
        "posting_date": posting.isoformat() if posting else None,
        "reason": reason,
    }
    # Surface any owed dates this run deliberately skipped, so the operator can
    # see (and if wanted, backfill with --posting-date) what was passed over.
    if posting is not None and last_posted is not None:
        skipped, d = [], last_posted + timedelta(days=1)
        while d < posting:
            skipped.append(d.isoformat())
            d += timedelta(days=1)
        if skipped:
            decision["skipped_owed_dates"] = skipped
    return posting, decision


def cmd_fetch(args):
    cutoff = _parse_cutoff(args.cutoff)

    # Always needed: the staleness guard below cross-checks the paper we are about
    # to serve against the newest posting already recorded in the ledger.
    last_posted = _last_posted_date(args.ledger)

    if args.posting_date:
        posting = datetime.strptime(args.posting_date, "%Y-%m-%d").date()
        decision = {"forced_posting_date": args.posting_date,
                    "reason": "explicit --posting-date override"}
    else:
        posting, decision = decide_posting_date(_ist_now(), cutoff, last_posted)
        if posting is None:
            print(json.dumps({
                "ok": False, "nothing_due": True,
                "date_decision": decision,
                "reason": "Nothing due yet — already caught up for the allowed window.",
            }, ensure_ascii=False))
            return 3

    # Search backwards for the newest available paper, starting the day BEFORE
    # the posting date and going back max_back days (handles weekends).
    start = posting - timedelta(days=1)
    attempts = []
    for i in range(args.max_back + 1):
        d = start - timedelta(days=i)
        ok, url, payload, tried = _try_download(d)
        attempts.append({"date": d.isoformat(), "url": url,
                         "result": "ok" if ok else payload,
                         "tried": tried})
        if ok:
            gap = (posting - d).days
            expected = posting - timedelta(days=1)

            # STALENESS GUARD — never silently serve a paper an earlier posting
            # already consumed. The paper for posting date D must be dated D-1; if
            # we fell back to one dated BEFORE last_posted, that paper was already
            # mined for a previous day's posts, so re-serving it would republish
            # yesterday's prices under today's date. Fail loudly instead.
            stale = last_posted is not None and d < last_posted
            if stale and not args.allow_stale_pdf:
                print(json.dumps({
                    "ok": False,
                    "pdf_not_resolvable": True,
                    "stale_pdf": True,
                    "posting_date": posting.isoformat(),
                    "expected_pdf_date": expected.isoformat(),
                    "stale_pdf_date": d.isoformat(),
                    "stale_pdf_url": url,
                    "last_posted": last_posted.isoformat(),
                    "gap_days": gap,
                    "weekend_fallback": _no_paper_gap(d, posting),
                    "reason": (
                        f"Paper for {expected.isoformat()} is not resolvable at any known "
                        f"filename variant, and the newest paper found ({d.isoformat()}) predates "
                        f"last_posted ({last_posted.isoformat()}), so it was already used for an "
                        f"earlier posting. Refusing to serve a stale paper. Either wait for the "
                        f"paper to be published, pass the real URL manually, add its filename "
                        f"variant to FILENAME_SUFFIXES, or re-run with --allow-stale-pdf to "
                        f"override deliberately."),
                    "date_decision": decision,
                    "attempts": attempts,
                }, ensure_ascii=False))
                return 4

            pdf_dir = os.path.join(BASE_DIR, "pdfs")
            os.makedirs(pdf_dir, exist_ok=True)
            fname = os.path.basename(url)  # exact server filename incl. its casing
            path = os.path.join(pdf_dir, fname)
            with open(path, "wb") as f:
                f.write(payload)
            out = {
                "ok": True, "path": path, "url": url,
                "posting_date": posting.isoformat(),
                "pdf_date_used": d.isoformat(),
                "expected_pdf_date": expected.isoformat(),
                "gap_days": gap,
                # weekend_fallback now means what its name says: the only skipped
                # dates are Sundays (no VK edition). Use older_paper_used for the
                # raw "gap > 1" signal this field used to carry.
                "weekend_fallback": _no_paper_gap(d, posting),
                "older_paper_used": gap > 1,
                "stale_pdf": bool(stale),
                "bytes": len(payload),
                "date_decision": decision,
                "attempts": attempts,
            }
            if stale:
                out["warning"] = (
                    f"STALE PAPER SERVED under --allow-stale-pdf: {d.isoformat()} predates "
                    f"last_posted {last_posted.isoformat()} and was already used for an earlier "
                    f"posting. Do NOT publish commodity data from it as fresh.")
            print(json.dumps(out, ensure_ascii=False))
            return 0

    print(json.dumps({
        "ok": False,
        "pdf_not_resolvable": True,
        "stale_pdf": False,
        "posting_date": posting.isoformat(),
        "expected_pdf_date": (posting - timedelta(days=1)).isoformat(),
        "reason": f"No VK PDF found within {args.max_back} days before posting date",
        "date_decision": decision,
        "attempts": attempts,
    }, ensure_ascii=False))
    return 2


def main():
    ap = argparse.ArgumentParser(description="Fetch the latest VK PDF + decide posting date (poster is Untitled.py)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pf = sub.add_parser("fetch", help="download the newest available VK PDF")
    pf.add_argument("--posting-date", help="YYYY-MM-DD (override; default: decided from ledger + IST time)")
    pf.add_argument("--max-back", type=int, default=4,
                    help="how many days back to search for a paper (default 4, covers weekends)")
    pf.add_argument("--cutoff", default="18:00",
                    help="IST cutoff HH:MM; at/after = next-day run, before = same-day run (default 18:00; the cloud routine fires ~7:06 PM so this must be below that)")
    pf.add_argument("--ledger", default=DEFAULT_LEDGER,
                    help="path to the dedup ledger that records posted dates")
    pf.add_argument("--allow-stale-pdf", action="store_true",
                    help="override the staleness guard and serve a paper that predates the "
                         "newest ledger posting (i.e. one already used). Off by default; the "
                         "run then exits 4 instead of silently republishing old prices.")
    pf.set_defaults(func=cmd_fetch)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
