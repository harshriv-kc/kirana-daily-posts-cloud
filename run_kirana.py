#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_kirana.py — fetch the latest available व्यापार केसरी (VK) PDF for the
kirana daily-posts routine, and decide WHICH posting date this run is for.

DATE LOGIC — MORNING-ONLY:
  posting_date is ALWAYS today (IST). The routine fires at 07:00 IST on the very
  day it posts for, so run date == posting date. There is no next-day branch and
  no cutoff: a run that fires late (delay, retry, manual kick at 21:00) still
  publishes TODAY, never tomorrow — publishing tomorrow's date is the retired
  evening behaviour and would also burn the next day's slot.
  --cutoff is still accepted but IGNORED, so old callers do not break.

  1. last_posted = newest `date` recorded in the dedup ledger
                   (kirana-used-log.json -> runs[].date = posting_date).
  2. posting_date:
        - last_posted <  today -> posting_date = today   (post; skip any stale
                                                          owed dates in between)
        - last_posted >= today -> NOTHING DUE (today already published; the next
                                 run is tomorrow 07:00 IST)

  Why NOT gap-fill (fixed 27-Jul-2026): backfilling the oldest owed date makes a
  single missed run permanent. The Sat 25-Jul-2026 evening run was missed, so the
  Sun 26-Jul run filled 26-Jul (same day) instead of 27-Jul — and every later
  evening run would have kept filling the stale owed date, leaving the routine
  exactly one day behind forever. Skipping the stale date(s) keeps it current;
  any skipped dates are reported in date_decision.skipped_owed_dates.
  To deliberately publish a missed day, run with --posting-date YYYY-MM-DD.

  Catch-up still works: a run that fires late on the 28th (or at 2 AM, or on a
  retry) still produces the 28th, because posting_date is simply today.

  Examples (morning-only):
    - 28th 07:00, ledger last=27th -> post 28  (normal morning run)
    - 28th 07:00, ledger last=25th -> post 28  (skip stale 26,27; stay current)
    - 28th 21:00, ledger last=27th -> post 28  (late run STILL posts today, not 29)
    - 28th 07:00, ledger last=28th -> NOTHING DUE (today already published)

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

# Guessing filenames cannot tell "no paper was published" apart from "published
# under a name we did not guess" — both look like a 404. Real names do carry
# surprises the template misses, e.g. VK-18-AUGUST-2026-1.pdf and
# VK-14-August-2026-1.pdf (a re-upload suffix). WordPress exposes its media
# library over REST, which returns the EXACT source_url whatever the naming, so
# we ask it first and keep the guessing below as an offline fallback.
MEDIA_API = "https://vyaparkesari.com/wp-json/wp/v2/media"
MEDIA_TIMEOUT = 30


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


def _media_urls_for(d):
    """Ask the site's media library which VK PDF actually exists for date d.

    Returns (urls_newest_upload_first, api_reachable). An empty list with
    api_reachable True is a POSITIVE result: the publisher genuinely has not
    uploaded that day's PDF, so a stale-paper fallback is correct rather than a
    naming miss we should have caught. Never raises — on any network/parse
    problem it degrades to (…, False) and the caller falls back to guessing.
    """
    params = {
        "mime_type": "application/pdf",
        # Cover-date-D issues are uploaded the evening of D-1, occasionally on D
        # itself; a generous window costs nothing and tolerates late uploads.
        "after": (d - timedelta(days=4)).isoformat() + "T00:00:00",
        "before": (d + timedelta(days=2)).isoformat() + "T00:00:00",
        "per_page": 50,
        "orderby": "date",
        "order": "desc",
    }
    try:
        r = requests.get(MEDIA_API, params=params, headers=HEADERS, timeout=MEDIA_TIMEOUT)
        if r.status_code != 200:
            return [], False
        items = r.json()
        if not isinstance(items, list):
            return [], False
    except Exception:
        return [], False

    # VK-<d|dd>-<Month any case>-<yyyy>[-N].pdf — the -N suffix is a re-upload.
    pat = re.compile(
        r"^VK-0?{day}-{month}-{year}(?:-\d+)?\.pdf$".format(
            day=d.day, month=re.escape(d.strftime("%B")), year=d.year),
        re.IGNORECASE,
    )
    urls = []
    for m in items:
        src = (m or {}).get("source_url") or ""
        if src and pat.match(os.path.basename(src)):
            urls.append(src)
    return urls, True


def _try_download(d):
    """Resolve and download date d's PDF.

    Returns (ok, url, payload_or_errsummary, tried, absent_confirmed).
    `url` is the working URL on success (exact server casing), else the first tried.
    `tried` lists each attempt so callers can log what was probed.
    `absent_confirmed` is True only when the media API answered and holds no PDF
    for d — i.e. the paper is genuinely unpublished, not merely unguessable."""
    tried = []
    media_urls, api_ok = _media_urls_for(d)
    absent_confirmed = api_ok and not media_urls
    # Media-library hits first (authoritative), then the guessed names as backup.
    urls = media_urls + [u for u in _urls_for(d) if u not in media_urls]
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
        return True, url, r.content, tried, absent_confirmed
    summary = "; ".join(f"{t['url'].rsplit('/', 1)[-1]}={t['result']}" for t in tried)
    if absent_confirmed:
        summary = "media library has no PDF for this date (not published); " + summary
    return False, urls[0], summary, tried, absent_confirmed


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


def decide_posting_date(now_ist, cutoff=None, last_posted=None):
    """Return (posting_date_or_None, decision_dict). None => nothing due yet.

    MORNING-ONLY: the posting date is ALWAYS today (IST). The routine fires at
    07:00 IST on the day it is posting for, so run date == posting date, full
    stop. There is no next-day branch and no cutoff any more: a run that fires
    late (delay, retry, manual kick at 21:00) must still publish TODAY, never
    tomorrow. Publishing tomorrow's date is the retired evening behaviour and
    would also burn the next day's slot.

    `cutoff` is accepted and ignored; it only exists so older callers passing
    --cutoff do not break.
    """
    today = now_ist.date()

    if last_posted is None:
        # No history: post today.
        posting = today
        reason = "no ledger history -> post today (morning-only)"
    elif last_posted < today:
        # STAY CURRENT: a missed run leaves a stale owed date behind. Backfilling
        # it publishes yesterday's date today and keeps the routine one day behind
        # forever, so skip the stale date(s) and post today.
        # (To deliberately publish a missed day, use --posting-date.)
        posting = today
        reason = ("skipped stale owed date(s) to stay current"
                  if last_posted < today - timedelta(days=1)
                  else "normal morning run")
    else:
        # last_posted >= today: today is already published.
        posting = None
        reason = ("already posted for today; morning-only routine never targets "
                  "tomorrow, so nothing is due until tomorrow 07:00 IST")

    decision = {
        "now_ist": now_ist.isoformat(timespec="seconds"),
        "mode": "morning-only (posting_date is always today IST)",
        "today_ist": today.isoformat(),
        "max_allowed": today.isoformat(),
        "last_posted": last_posted.isoformat() if last_posted else None,
        "next_owed": (last_posted + timedelta(days=1)).isoformat() if last_posted else None,
        "last_posted_is_today": bool(last_posted and last_posted >= now_ist.date()),
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
    skipped_unpublished = []   # dates the media library confirms have no PDF at all
    for i in range(args.max_back + 1):
        d = start - timedelta(days=i)
        ok, url, payload, tried, absent_confirmed = _try_download(d)
        attempts.append({"date": d.isoformat(), "url": url,
                         "result": "ok" if ok else payload,
                         "not_published": absent_confirmed,
                         "tried": tried})
        if not ok and absent_confirmed:
            skipped_unpublished.append(d.isoformat())
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
                # Dates skipped because the publisher never uploaded a PDF for
                # them (media library confirms absence) — distinguishes a real
                # publisher gap from a filename we failed to guess.
                "not_published_dates": skipped_unpublished,
                "bytes": len(payload),
                "date_decision": decision,
                "attempts": attempts,
            }, ensure_ascii=False))
            return 0

    print(json.dumps({
        "ok": False,
        "posting_date": posting.isoformat(),
        "reason": f"No VK PDF found within {args.max_back} days before posting date",
        "not_published_dates": skipped_unpublished,
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
