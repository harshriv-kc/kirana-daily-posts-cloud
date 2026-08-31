#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deadline_check.py — the ONLY authority on whether the 08:00 IST सोया तेल
deadline has been missed.

WHY THIS EXISTS
---------------
On 2026-08-20, 08-21, 08-22, 08-23, 08-24 and 08-30 the routine sent Harsh a
"सोया तेल will miss the 08:00 slot" Slack DM and then, minutes later, reported
that सोया तेल had gone live comfortably on time. Six false alarms in eleven
days, each followed by a correction DM.

The cause was always the same: the agent ESTIMATED how much wall-clock time had
passed instead of READING a clock. Tool calls feel like minutes but take
seconds, so the running estimate drifted 20-40 minutes ahead of reality, and the
agent "knew" it had slipped while it was in fact still half an hour early.

The spec's trigger is a FACT, not a forecast: "सोया तेल is not live by 08:00
IST". That cannot be true before 08:00. Never DM on a prediction.

USAGE
-----
    python deadline_check.py

Exit codes / verdicts (the verdict line is what you act on):

  PENDING       सोया तेल not live yet, but it is still before 08:00 IST.
                --> DO NOT DM. There is nothing to report. Keep working.
  ON_TIME       सोया तेल published before 08:00 IST. --> DO NOT DM.
  LATE_LIVE     सोया तेल published, but after 08:00 IST.
                --> DM Harsh with the real timestamp printed below.
  SLIPPED       It is past 08:00 IST and सोया तेल is still not live.
                --> DM Harsh NOW with the real timestamp printed below.

Only LATE_LIVE and SLIPPED authorise a Slack DM to Harsh (U09K92G1U1X).
"""
import json
import os
import re
import sys
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
DEADLINE = time(8, 0)
FIRST_POST = "सोया तेल"


def ist_now():
    return datetime.now(IST)


def local_to_ist(naive_local):
    """Poster logs use datetime.now() (container-local, normally UTC).
    Attach the real local offset and convert to IST — never hardcode +5:30."""
    local_tz = datetime.now().astimezone().tzinfo
    return naive_local.replace(tzinfo=local_tz).astimezone(IST)


def published_at_ist(date_str):
    """Return the IST datetime सोया तेल was published, or None."""
    log_path = f"post_{date_str}.log"
    if not os.path.exists(log_path):
        return None
    pat = re.compile(
        r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+PUBLISHED\s+" + re.escape(FIRST_POST)
    )
    with open(log_path, encoding="utf-8") as fh:
        for line in fh:
            m = pat.search(line)
            if m:
                return local_to_ist(datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"))
    return None


def state_status(date_str):
    path = f"post_state_{date_str}.json"
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            state = json.load(fh)
        return state.get("items", {}).get(FIRST_POST, {}).get("status")
    except (OSError, ValueError):
        return None


def main():
    now = ist_now()
    date_str = now.strftime("%Y-%m-%d")
    deadline_dt = datetime.combine(now.date(), DEADLINE, tzinfo=IST)
    mins_left = (deadline_dt - now).total_seconds() / 60.0

    status = state_status(date_str)
    pub_ist = published_at_ist(date_str)

    print(f"IST now            : {now:%Y-%m-%d %H:%M:%S} IST")
    print(f"08:00 deadline     : {deadline_dt:%H:%M} IST")
    if mins_left >= 0:
        print(f"Time remaining     : {mins_left:.1f} min")
    else:
        print(f"Past deadline by   : {abs(mins_left):.1f} min")
    print(f"{FIRST_POST} state     : {status or 'not attempted yet'}")
    if pub_ist:
        print(f"{FIRST_POST} live at   : {pub_ist:%H:%M:%S} IST")

    if pub_ist is not None:
        if pub_ist <= deadline_dt:
            verdict, action = "ON_TIME", "DO NOT DM. Deadline met."
        else:
            verdict, action = (
                "LATE_LIVE",
                f"DM Harsh (U09K92G1U1X): सोया तेल went live {pub_ist:%H:%M:%S} IST, "
                f"{abs((pub_ist - deadline_dt).total_seconds()) / 60:.0f} min after 08:00.",
            )
    elif now <= deadline_dt:
        verdict, action = (
            "PENDING",
            f"DO NOT DM. Still {mins_left:.1f} min before the 08:00 slot — "
            "a slip has NOT happened and must not be predicted.",
        )
    else:
        verdict, action = (
            "SLIPPED",
            f"DM Harsh (U09K92G1U1X) NOW: it is {now:%H:%M:%S} IST and "
            f"{FIRST_POST} is still not live.",
        )

    print(f"VERDICT            : {verdict}")
    print(f"ACTION             : {action}")
    return 0 if verdict in ("ON_TIME", "PENDING") else 1


if __name__ == "__main__":
    sys.exit(main())
