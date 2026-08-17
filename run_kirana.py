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
  3. max_allowed = the furthest date this run may target, based on IST clock and
     the --cutoff (default 18:00 IST):
        - run fires AT/AFTER the cutoff -> max_allowed = today + 1  (next-day run)
        - run fires BEFORE   the cutoff -> max_allowed = today      (same-day run)
     The routine now fires at 07:00 IST ON THE POSTING DAY, which is before the
     cutoff, so max_allowed = today and posting_date = today. Keep the cutoff
     ABOVE 07:00 or the morning run would target tomorrow instead.
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

LATEST-PAPER RULE: PDF used = the newest VK paper published by run time, searched
backwards from the POSTING DATE ITSELF (not posting_date - 1). Whatever the clock
says, the run always drafts from the freshest issue on the server.

  Upload window, measured from Last-Modified over 26 issues (Jul-Aug 2026): the
  paper cover-dated D goes live between 21:39 and 23:38 IST on D-1, median ~22:20.
  Sunday editions are never published; the publisher also skips the odd weekday.

  -> CURRENT SCHEDULE, 07:00 IST on day D: the cover-date-D paper is ~8h old and
     is taken straight away. gap_days == 0. Hit rate 25/26 days (96%), with 5.9h
     of margin against the latest observed upload. MORNING ONLY - the old ~19:06
     IST evening run is RETIRED.
  -> the retired evening run (~19:06 on D-1) could only ever see the D-1 paper,
     because the cover-date-D issue lands ~3h after it. gap_days == 1.

  The first user-visible post (सोया तेल) must be live by 08:00 IST, i.e. the whole
  pipeline has one hour. If it slips past 08:00, DM Harsh (U09K92G1U1X) at once so
  he can adjust the visible time by hand.

gap_days = posting_date - pdf_date_used. weekend_fallback = gap_days > 1.

STALE REUSE: when the newest available paper is the same issue an earlier run
already used (unavoidable when the publisher skips a day), `stale_reuse` is true
and `already_used_on` names that run. This is NOT an error and NOT a reason to
skip the day — post anyway, but change every dedup axis (Samachar hero, oil
frame/direction, dal/shakkar pick, other pick, Rujhan quiz commodity, both
trending themes, scheme). See specs/kirana-posts-content.md.

Posting itself is done by the existing Untitled.py (operator's poster) — NOT here.

Usage:
  python run_kirana.py fetch [--posting-date YYYY-MM-DD] [--max-back 4]
                             [--cutoff HH:MM] [--ledger PATH]
      Decides the posting date (unless --posting-date forces it), downloads the
      newest available VK PDF to ./pdfs/, and prints one JSON line:
        {"ok":true,"path":...,"url":...,"posting_date":"YYYY-MM-DD",
         "pdf_date_used":"YYYY-MM-DD","gap_days":N,"weekend_fallback":bool,
         "date_decision":{...},...}
      If nothing is due yet, prints {"ok":false,"nothing_due":true,...} and exits 3.
      Exits 2 only if NO paper is found within max-back days.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone, time as dtime, date as ddate

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IST = timezone(timedelta(hours=5, minutes=30))
DEFAULT_LEDGER = os.path.join(BASE_DIR, "kirana-used-log.json")

# vyaparkesari.com filenames are named INCONSISTENTLY by whoever uploads them:
# the English month token varies in case day-to-day within the same folder, e.g.
#   VK-04-JULY-2026.pdf   (uppercase)   but   VK-06-July-2026.pdf   (title-case).
# There is no reliable rule, so we PROBE every casing per date and use whichever
# returns a real PDF, instead of guessing one filename (which silently 404'd and
# fell back to a stale older paper).
URL_TMPL = "https://vyaparkesari.com/palaheeh/{yyyy}/{mm}/VK-{dd}-{MONTH}-{yyyy}.pdf"
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://vyaparkesari.com/"}
MIN_PDF_BYTES = 500_000  # a real VK PDF is multi-MB; guard against error pages


def _ist_now():
    return datetime.now(IST)


def _urls_for(d):
    """Candidate URLs for date d across every naming variation the site actually uses.
    Two independent inconsistencies, confirmed by auditing Jun-Jul 2026 filenames:
      - month-name CASE varies day to day: VK-04-JULY vs VK-06-July.
      - the day is sometimes zero-padded, sometimes not: VK-08-... vs VK-8-... .
    So we probe {padded, unpadded} day x {UPPER, Title, lower} month and use
    whichever returns a real PDF. (No abbreviated month like 'Jul' was ever
    observed, so full month name only.) Dedup, order-preserving."""
    yyyy, mm = d.strftime("%Y"), d.strftime("%m")
    days = [d.strftime("%d"), str(d.day)]            # e.g. "08" and "8" (same for >=10)
    month = d.strftime("%B")                          # full English month, e.g. "July"
    months = [month.upper(), month.capitalize(), month.lower()]
    urls, seen = [], set()
    for day in days:
        for mon in months:
            u = URL_TMPL.format(yyyy=yyyy, mm=mm, dd=day, MONTH=mon)
            if u not in seen:
                seen.add(u)
                urls.append(u)
    return urls


def _try_download(d):
    """Probe every casing for date d. Returns (ok, url, payload_or_errsummary, tried).
    `url` is the working URL on success (exact server casing), else the first tried.
    `tried` lists each casing attempt so callers can log what was probed."""
    tried = []
    urls = _urls_for(d)
    for url in urls:
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


def _previously_used_pdfs(ledger_path):
    """{lowercased VK filename -> posting_date that already used it}.

    Lets a run detect that the newest published paper is the SAME issue a previous
    run already drafted from (happens whenever the publisher skips a day — always
    on Sundays). Reads the explicit `pdf_used` field, falling back to scraping the
    filename out of `_note` for entries written before that field existed.
    """
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    seen = {}
    for run in data.get("runs", []):
        names = []
        if run.get("pdf_used"):
            names.append(str(run["pdf_used"]))
        names += re.findall(r"VK-\d{1,2}-[A-Za-z]+-\d{4}\.pdf", str(run.get("_note", "")))
        for n in names:
            seen.setdefault(n.lower(), set()).add(run.get("date"))
    return {k: sorted(d for d in v if d) for k, v in seen.items()}


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

    if args.posting_date:
        posting = datetime.strptime(args.posting_date, "%Y-%m-%d").date()
        decision = {"forced_posting_date": args.posting_date,
                    "reason": "explicit --posting-date override"}
    else:
        last_posted = _last_posted_date(args.ledger)
        posting, decision = decide_posting_date(_ist_now(), cutoff, last_posted)
        if posting is None:
            print(json.dumps({
                "ok": False, "nothing_due": True,
                "date_decision": decision,
                "reason": "Nothing due yet — already caught up for the allowed window.",
            }, ensure_ascii=False))
            return 3

    # LATEST-PAPER RULE: always use the newest VK paper published at run time.
    # Search starts AT the posting date (not the day before) and walks back, so a
    # run that fires after the publisher's upload window automatically picks up the
    # fresher paper instead of yesterday's. Upload window (measured over 26 issues,
    # Jul-Aug 2026 Last-Modified headers): the paper cover-dated D goes live between
    # 21:39 and 23:38 IST on D-1, median ~22:20. So:
    #   - CURRENT: 07:00 IST on day D -> cover-date-D paper IS up (~8h old); the
    #     search hits it immediately. gap_days == 0. 96% of days.
    #   - RETIRED evening slot (~19:06 on D-1) -> cover-date-D paper NOT up yet
    #     (lands ~3h later); search fell through to D-1. gap_days == 1.
    # Sunday editions never exist, so a Monday posting date legitimately falls back.
    start = posting
    attempts = []
    used_before = _previously_used_pdfs(args.ledger)
    for i in range(args.max_back + 1):
        d = start - timedelta(days=i)
        ok, url, payload, tried = _try_download(d)
        attempts.append({"date": d.isoformat(), "url": url,
                         "result": "ok" if ok else payload,
                         "tried": tried})
        if ok:
            pdf_dir = os.path.join(BASE_DIR, "pdfs")
            os.makedirs(pdf_dir, exist_ok=True)
            fname = os.path.basename(url)  # exact server filename incl. its casing
            path = os.path.join(pdf_dir, fname)
            with open(path, "wb") as f:
                f.write(payload)
            gap = (posting - d).days
            prior = used_before.get(fname.lower())
            print(json.dumps({
                "ok": True, "path": path, "url": url,
                "posting_date": posting.isoformat(),
                "pdf_date_used": d.isoformat(),
                "pdf_used": fname,
                "gap_days": gap,
                "weekend_fallback": gap > 1,
                # STALE REUSE: this exact issue already produced a previous run.
                # Not an error — post anyway, but every dedup axis MUST change.
                "stale_reuse": prior is not None,
                "already_used_on": prior,
                "bytes": len(payload),
                "date_decision": decision,
                "attempts": attempts,
            }, ensure_ascii=False))
            return 0

    print(json.dumps({
        "ok": False,
        "posting_date": posting.isoformat(),
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
                    help="IST cutoff HH:MM; at/after = next-day run, before = same-day run (default 18:00). The routine now fires 07:00 IST on the POSTING DAY, so the cutoff must stay ABOVE 07:00 for that to count as a same-day run. Do not lower it below 07:00.")
    pf.add_argument("--ledger", default=DEFAULT_LEDGER,
                    help="path to the dedup ledger that records posted dates")
    pf.set_defaults(func=cmd_fetch)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
