"""
Post the daily Kirana items to the D2R postAutomation API.

DESIGN RULE #1 — AT MOST ONCE. NEVER TWICE.
-------------------------------------------
On 2026-08-19 the Samachar post was published twice. Cause: the egress proxy
severs any request at ~300s, so the response was lost; the outcome was unknown;
the item was sent a second time; both sends had in fact reached the backend and
each created a post.

So this script treats "sent" — not "succeeded" — as the irreversible act:

  * A per-day state file records every item BEFORE its request goes out, and is
    fsynced to disk so a SIGKILL cannot lose it.
  * An item that has EVER been attempted is never sent again automatically.
    Not on resume, not after a crash, not after a lost response.
  * Re-sending is only possible by a human passing --force <post_name>, after
    they have looked at the feed and confirmed the post is not there.

That makes a duplicate structurally impossible rather than merely unlikely.

DESIGN RULE #2 — NEVER LOSE ANYTHING THE BACKEND GAVE US.
---------------------------------------------------------
The old script only wrote its results file after all 8 items finished, so when
the process was killed mid-run the itemID of the already-published सोया तेल post
was lost with it. Every result is now persisted the moment it arrives.

The same rule was being broken more quietly until 2026-09-11: extract_ids()
picked out only item_id/d2r_link and threw the rest of the response away, so the
thumbnail URLs (expanded_image_url / collapsed_image_url) the backend had
already handed us were unrecoverable, and the daily Slack post could only carry
D2R links. Those two URLs are now captured as first-class fields, AND the whole
data[0] object is kept under "response" so a field added server-side tomorrow is
never lost again.

Usage:
    python post_items.py                      # send everything not yet attempted
    python post_items.py --status             # print the ledger, send nothing
    python post_items.py --links              # print the Slack asset-links block
    python post_items.py --force "Samachar"   # deliberate re-send, human-checked
"""
import argparse
import json
import os
import sys
import traceback
from datetime import datetime

import requests

API_URL = "https://asia-south1-op-d2r.cloudfunctions.net/postAutomation"
INPUT_FILE = "request_body.json"

# The proxy severs at ~300s. Give up at 295s so we record a clean PROXY_CUT
# instead of an opaque stack trace — the request may still land server-side,
# which is exactly why such an item is never retried.
REQUEST_TIMEOUT = 295

ST_PENDING = "PENDING"    # never attempted — safe to send
ST_SENT = "SENT"          # request went out; outcome not yet known
ST_PUBLISHED = "PUBLISHED"  # confirmed created, itemID captured
ST_UNKNOWN = "UNKNOWN"    # response lost — MAY OR MAY NOT EXIST. Never auto-retried.
ST_REJECTED = "REJECTED"  # backend explicitly said it did not create the post


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    line = f"[{ts()}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as lf:
        lf.write(line + "\n")


def save_state(state):
    """Write + fsync the ledger. Must survive SIGKILL — it is the duplicate guard."""
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, STATE_FILE)


ENTRY_FIELDS = {
    "status": ST_PENDING, "attempts": 0, "item_id": None, "d2r_link": None,
    "expanded_image_url": None, "collapsed_image_url": None,
    "response": None, "detail": None, "elapsed": None,
}


def load_state(posts):
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"date": TODAY, "items": {}}

    for i, p in enumerate(posts, start=1):
        name = p.get("post_name", f"item{i}")
        entry = state["items"].setdefault(name, {"order": i})
        # Also back-fills fields added in a later version onto an older state
        # file, so a mid-run resume never KeyErrors on a new key.
        for k, v in ENTRY_FIELDS.items():
            entry.setdefault(k, v)
        entry.setdefault("order", i)
    return state


def _clean_url(value):
    """Normalise a URL the backend handed us.

    Strips Slack-style <...> wrapping and surrounding whitespace. CDN query
    params are deliberately NOT stripped here — this is the archival record;
    trimming for display happens in slack_links().
    """
    if not isinstance(value, str):
        return None
    v = value.strip().lstrip("<").rstrip(">").strip()
    return v or None


def extract_ids(resp_data):
    """Pull (item_id, d2r_link, ok, detail, images, raw) out of a response body.

    HTTP 200 is NOT proof of creation: the backend answers 200 with
    success:false when the downstream News API fails.

    `images` is a dict of the two thumbnail URLs (either may be None — some
    posts genuinely come back without them, which is normal and not an error).
    `raw` is the whole data[0] object, kept so that a field we do not yet know
    about is still on disk tomorrow.
    """
    empty = {"expanded_image_url": None, "collapsed_image_url": None}
    posts = (resp_data or {}).get("data")
    if isinstance(posts, list) and posts:
        p = posts[0]
        ok = bool(p.get("success"))
        link = _clean_url(p.get("d2r_link") or p.get("link")) or ""
        item_id = p.get("itemId") or p.get("item_id") or p.get("id")
        if not item_id and link:
            item_id = link.rstrip("/").rsplit("/", 1)[-1]  # .../article/view/<uuid>
        images = {
            # snake_case is what the API returns today; the camelCase spellings
            # are accepted defensively because itemId already arrives camelCase.
            "expanded_image_url": _clean_url(
                p.get("expanded_image_url") or p.get("expandedImageUrl")),
            "collapsed_image_url": _clean_url(
                p.get("collapsed_image_url") or p.get("collapsedImageUrl")),
        }
        detail = None if ok else (p.get("error") or "success=false")
        return item_id, link, ok, detail, images, p
    if (resp_data or {}).get("success") is False:
        return (None, None, False,
                str((resp_data or {}).get("message") or "success=false"), empty, None)
    return None, None, False, "unrecognised response shape", empty, None


def _display_url(url):
    """CDN query params are dropped for display — the clean .webp opens fine and
    it keeps the Slack message well under the 5000-char limit."""
    return url.split("?", 1)[0] if url else None


def slack_links(state, posts):
    """Render the STEP 9b asset-links block for #inhouse-content.

    One line per post carrying all of that post's assets, in posting order.
    A post with no image URLs simply omits those links (normal, not flagged);
    a post that did not publish is written as failed with no links.
    """
    order = sorted(state["items"].items(), key=lambda kv: kv[1]["order"])
    n_live = sum(1 for _, it in order if it["status"] == ST_PUBLISHED)
    day = datetime.strptime(state.get("date", TODAY), "%Y-%m-%d").strftime("%-d %b")

    lines = [f"**📰 Daily Posts · {day}** — {n_live}/{len(posts)} live"]
    for name, it in order:
        if it["status"] != ST_PUBLISHED:
            lines.append(f"{it['order']}. {name} — ❌ failed")
            continue
        parts = []
        if it.get("d2r_link"):
            parts.append(f"[D2R]({_display_url(it['d2r_link'])})")
        for label, key in (("exp", "expanded_image_url"),
                           ("col", "collapsed_image_url")):
            if it.get(key):
                parts.append(f"[{label}]({_display_url(it[key])})")
        lines.append(f"{it['order']}. {name} — " + " · ".join(parts))
    return "\n".join(lines)


def report(state, posts):
    log("=" * 72)
    log("LEDGER")
    order = sorted(state["items"].items(), key=lambda kv: kv[1]["order"])
    for name, it in order:
        line = f"  {it['order']}. {name:<28} {it['status']:<10}"
        if it.get("d2r_link"):
            line += f" {it['d2r_link']}"
        elif it.get("detail"):
            line += f" ({it['detail']})"
        log(line)
        imgs = [f"{lbl}={it[k]}" for lbl, k in (("exp", "expanded_image_url"),
                                                ("col", "collapsed_image_url"))
                if it.get(k)]
        if imgs:
            log(" " * 44 + "  ".join(imgs))

    published = [n for n, i in order if i["status"] == ST_PUBLISHED]
    unknown = [n for n, i in order if i["status"] in (ST_SENT, ST_UNKNOWN)]
    rejected = [n for n, i in order if i["status"] == ST_REJECTED]
    pending = [n for n, i in order if i["status"] == ST_PENDING]

    log("-" * 72)
    log(f"PUBLISHED (itemID captured): {len(published)}/{len(posts)}")
    if rejected:
        log(f"REJECTED by backend: {len(rejected)} -> {', '.join(rejected)}")
    if pending:
        log(f"NOT SENT: {len(pending)} -> {', '.join(pending)}")
    if unknown:
        log("")
        log(f"!! MANUAL CHECK REQUIRED: {len(unknown)} item(s) were sent once but the")
        log("!! response was lost. They may or may not be live. They will NOT be")
        log("!! retried automatically — that is what prevents a duplicate.")
        for n in unknown:
            log(f"!!   - {n}")
        log("!! Look at the feed. If one is genuinely missing, publish it with:")
        log(f'!!   python post_items.py --force "{unknown[0]}"')
    log("=" * 72)
    return len(published), unknown, rejected, pending


def main():
    global LOG_FILE, STATE_FILE, TODAY

    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true",
                    help="print the ledger and exit without sending anything")
    ap.add_argument("--links", action="store_true",
                    help="print the Slack asset-links block and exit without "
                         "sending anything")
    ap.add_argument("--force", action="append", default=[], metavar="POST_NAME",
                    help="re-send one item whose outcome was unknown. Only after "
                         "checking the feed — this CAN create a duplicate.")
    args = ap.parse_args()

    TODAY = datetime.now().strftime("%Y-%m-%d")
    LOG_FILE = f"post_{TODAY}.log"
    STATE_FILE = f"post_state_{TODAY}.json"

    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        sys.exit(1)
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        request_body = json.load(f)
    if not isinstance(request_body, list):
        request_body = [request_body]

    state = load_state(request_body)

    if args.links:
        print(slack_links(state, request_body))
        return

    if args.status:
        LOG_FILE = os.devnull
        report(state, request_body)
        return

    log("=" * 72)
    log(f"Script started | input={INPUT_FILE} | items={len(request_body)}")
    log(f"State ledger: {STATE_FILE}")
    log(f"Client timeout {REQUEST_TIMEOUT}s (proxy severs at ~300s)")
    if args.force:
        log(f"FORCE re-send requested for: {args.force}")
    log("=" * 72)

    for i, item in enumerate(request_body, start=1):
        name = item.get("post_name", f"item{i}")
        entry = state["items"][name]

        if entry["status"] == ST_PUBLISHED:
            log(f"--- SKIP {i}/{len(request_body)} {name}: already published "
                f"({entry.get('d2r_link')})")
            continue

        if entry["status"] in (ST_SENT, ST_UNKNOWN) and name not in args.force:
            log(f"--- SKIP {i}/{len(request_body)} {name}: already sent once, outcome "
                f"unknown. NOT retrying (duplicate guard). Use --force to override.")
            continue

        if entry["status"] == ST_REJECTED and name not in args.force:
            log(f"--- SKIP {i}/{len(request_body)} {name}: backend rejected it "
                f"({entry.get('detail')}). Use --force to retry.")
            continue

        # Record the attempt BEFORE the request leaves. If we are killed between
        # here and the response, the item still reads as SENT and is never resent.
        entry["status"] = ST_SENT
        entry["attempts"] += 1
        entry["detail"] = "request in flight"
        save_state(state)

        log(f"--- Sending {i}/{len(request_body)} {name} (attempt {entry['attempts']}) ---")
        start = datetime.now()
        try:
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json=[item],
                timeout=REQUEST_TIMEOUT,
            )
            elapsed = (datetime.now() - start).total_seconds()
            entry["elapsed"] = round(elapsed, 2)

            try:
                resp_data = response.json()
            except json.JSONDecodeError:
                resp_data = {"raw_text": response.text}

            if response.status_code != 200:
                entry["status"] = ST_REJECTED
                entry["detail"] = f"HTTP {response.status_code}"
                log(f"REJECTED {name}: HTTP {response.status_code} ({elapsed:.1f}s)")
            else:
                item_id, link, ok, detail, images, raw = extract_ids(resp_data)
                # Keep what we were given even on rejection — a REJECTED item can
                # still carry a diagnostic payload worth reading afterwards.
                entry["response"] = raw
                entry.update(images)
                if ok:
                    entry["status"] = ST_PUBLISHED
                    entry["item_id"] = item_id
                    entry["d2r_link"] = link
                    entry["detail"] = None
                    log(f"PUBLISHED {name} ({elapsed:.1f}s) itemID={item_id}")
                    log(f"          {link}")
                    for label, key in (("exp", "expanded_image_url"),
                                       ("col", "collapsed_image_url")):
                        if images[key]:
                            log(f"          {label}: {images[key]}")
                    if not (images["expanded_image_url"]
                            or images["collapsed_image_url"]):
                        log("          (no image URLs returned — normal for some posts)")
                else:
                    entry["status"] = ST_REJECTED
                    entry["detail"] = detail
                    log(f"REJECTED {name}: {detail} ({elapsed:.1f}s)")

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError) as e:
            elapsed = (datetime.now() - start).total_seconds()
            entry["status"] = ST_UNKNOWN
            entry["elapsed"] = round(elapsed, 2)
            entry["detail"] = (
                f"response lost after {elapsed:.0f}s (proxy cut at ~300s). "
                f"The request reached the backend; the post MAY exist."
            )
            log(f"RESPONSE LOST {name} after {elapsed:.1f}s — treating as UNKNOWN, "
                f"will NOT retry. {type(e).__name__}")

        except Exception as e:
            elapsed = (datetime.now() - start).total_seconds()
            entry["status"] = ST_UNKNOWN
            entry["elapsed"] = round(elapsed, 2)
            entry["detail"] = f"{type(e).__name__}: {e}"
            log(f"ERROR {name} after {elapsed:.1f}s: {type(e).__name__}: {e}")
            log(traceback.format_exc())

        # Persist immediately — an itemID must never die with the process.
        save_state(state)

    n_pub, unknown, rejected, pending = report(state, request_body)

    with open(f"post_{TODAY}.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    if unknown or rejected or pending:
        sys.exit(2)


if __name__ == "__main__":
    main()
