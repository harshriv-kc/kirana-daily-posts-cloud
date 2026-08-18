import json
import requests
from datetime import datetime
import sys
import time
import os
import traceback


API_URL = "https://asia-south1-op-d2r.cloudfunctions.net/postAutomation"
INPUT_FILE = "request_body.json"

# WHY A LOST CONNECTION IS *NOT* A FAILED POST — read before "fixing" this.
#
# postAutomation (Hogwarts-CloudSpells/UTILITY/postAutomation) does everything
# synchronously inside one HTTP request: generate 1-2 Gemini images, build the
# notification, POST to the News API (step 4), write the success row to
# news_generation_logs (step 5), THEN answer us. It averages ~14.8 min and is
# provisioned for long runs.
#
# Something in the network path cuts the connection at ~300s (2026-08-18: three
# items died at 300.53s / 300.43s / 300.62s). Our timeout below is 600s and never
# fired — the far end hung up, which surfaces as ConnectionError, not Timeout.
# So RAISING THE TIMEOUT DOES NOTHING. That is not the bug.
#
# The important part: Cloud Functions does not abort when the caller disconnects.
# The function keeps running and, if it gets past step 4, the post IS CREATED and
# logged — we simply never see the receipt. A dropped connection therefore means
# "outcome unknown", NOT "did not publish".
#
# Hence: NEVER auto-retry a dropped connection. If the post was already created,
# a retry publishes a SECOND copy to the live feed. There is no client-side way
# to tell the two cases apart today, so we report the item as UNVERIFIED, exit
# non-zero, and let a human check before anything is re-sent.
#
# The real fix is server-side and is one of:
#   (a) accept an idempotency_key per post, look it up in news_generation_logs,
#       and return the existing post_id instead of creating a duplicate — this
#       makes retries safe and is the smaller change; or
#   (b) make the endpoint async: 202 + job_id immediately, work in the
#       background, add a GET status route the poster polls. Removes the
#       long-lived connection entirely.
# Until one of those ships, leave this at 0.
CONNECTION_RETRIES = 0          # 0 = never blind-retry a lost response
RETRY_BACKOFF_SECONDS = 15      # only used if a future idempotency_key makes
                                # retries safe; doubles per attempt


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    line = f"[{ts()}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as lf:
        lf.write(line + "\n")


def main():
    global LOG_FILE

    today = datetime.now().strftime("%Y-%m-%d")
    LOG_FILE = f"post_{today}.log"

    log("=" * 60)
    log("Script started")
    log(f"Log file: {LOG_FILE}")
    log(f"Input file: {INPUT_FILE}")
    log(f"Target API: {API_URL}")
    log("=" * 60)

    if not os.path.exists(INPUT_FILE):
        log(f"ERROR: Input file '{INPUT_FILE}' not found. Exiting.")
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        request_body = json.load(f)

    # Ensure we have a list of items
    if not isinstance(request_body, list):
        request_body = [request_body]

    total = len(request_body)
    log(f"Request body loaded successfully ({total} item(s))")

    results = []
    success_count = 0
    failed_items = []
    fail_count = 0
    unverified_items = []
    unverified_count = 0
    overall_start = datetime.now()

    for i, item in enumerate(request_body, start=1):
        attempt = 0
        while True:
            attempt += 1
            if attempt == 1:
                log(f"--- Sending item {i}/{total} ---")
            else:
                log(f"--- Sending item {i}/{total} (attempt {attempt}"
                    f"/{CONNECTION_RETRIES + 1}) ---")
            start_time = datetime.now()

            try:
                response = requests.post(
                    API_URL,
                    headers={"Content-Type": "application/json"},
                    json=[item],  # Send as single-item list to match original format
                    timeout=600,  # 10 minutes
                )

                elapsed = (datetime.now() - start_time).total_seconds()
                log(f"Item {i}/{total} responded: Status {response.status_code} ({elapsed:.2f}s)")

                try:
                    resp_data = response.json()
                except json.JSONDecodeError:
                    resp_data = {"raw_text": response.text}

                results.append({
                    "item_index": i,
                    "status_code": response.status_code,
                    "attempts": attempt,  # >1 means an earlier send was lost in
                                          # transit — check this post for a duplicate
                    "elapsed_seconds": round(elapsed, 2),
                    "response": resp_data,
                })

                # HTTP 200 is NOT proof the post was created. The backend answers 200
                # with {"success": false, "data":[{"success": false, "error": ...}]}
                # when the downstream News API fails (seen 2026-08-17: the रुझान post
                # came back 200 / "News API failed: API Error: 404" and was silently
                # counted as a success). Trust the body, not the status line.
                # ...and even a success=false body is not always a clean rejection.
                # postAutomation calls the News API itself; if THAT call loses its
                # response, the error it reports back carries no status/statusText
                # and reads "API Error: undefined - undefined: undefined". The News
                # API may still have created the post and scheduled its push
                # notification. Seen 2026-08-18 on दाल/शक्कर: reported failed, re-sent,
                # and users got a duplicate PN. Treat that signature as UNVERIFIED.
                item_errors = []
                lost_downstream = False
                if response.status_code != 200:
                    item_errors.append(f"HTTP {response.status_code}")
                else:
                    posts = (resp_data or {}).get("data")
                    if isinstance(posts, list) and posts:
                        for p in posts:
                            if not p.get("success"):
                                item_errors.append(
                                    f"{p.get('post_name') or 'post'}: "
                                    f"{p.get('error') or 'success=false'}")
                    elif (resp_data or {}).get("success") is False:
                        item_errors.append(str((resp_data or {}).get("message") or "success=false"))

                lost_downstream = any(
                    "undefined - undefined" in e or "API Error: undefined" in e
                    for e in item_errors)

                if item_errors and lost_downstream:
                    log(f"UNVERIFIED: Item {i}/{total} — {'; '.join(item_errors)}. "
                        f"That error carries no HTTP status, so the News API never "
                        f"answered postAutomation and MAY still have created this "
                        f"post and sent its PN. Check before re-sending.")
                    results[-1]["outcome"] = "unverified"
                    unverified_count += 1
                    unverified_items.append(
                        (i, item.get("post_name"), "News API gave no response"))
                elif item_errors:
                    fail_count += 1
                    failed_items.append((i, item_errors))
                    log(f"FAILED: Item {i}/{total} did NOT publish — {'; '.join(item_errors)}")
                else:
                    success_count += 1

                # The backend answered. Whatever it said is final — a success=false
                # body is a real rejection, not a transport blip, so never retry it.
                break

            except (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError) as e:
                elapsed = (datetime.now() - start_time).total_seconds()
                kind = ("TIMEOUT" if isinstance(e, requests.exceptions.Timeout)
                        else "CONNECTION ERROR")
                detail = "timed out" if kind == "TIMEOUT" else str(e)
                log(f"{kind}: Item {i}/{total} after {elapsed:.2f}s: {detail}")
                log(traceback.format_exc())

                if attempt <= CONNECTION_RETRIES:
                    wait = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                    log(f"WARNING: Item {i}/{total} lost its response in transit — the "
                        f"backend MAY have created this post already. Retrying in "
                        f"{wait}s ({CONNECTION_RETRIES - attempt + 1} left); check for "
                        f"DUPLICATES if it publishes.")
                    time.sleep(wait)
                    continue

                # Outcome unknown — see the note at the top of this file. The
                # backend very likely finished and created the post; we just lost
                # the receipt. Do NOT describe this as "did not publish" and do
                # NOT re-send it blindly, or the feed gets a duplicate.
                log(f"UNVERIFIED: Item {i}/{total} — {kind} after {elapsed:.2f}s. "
                    f"The backend keeps running after we disconnect, so this post "
                    f"MAY BE LIVE. Check news_generation_logs / the D2R panel "
                    f"BEFORE re-sending it.")
                results.append({"item_index": i,
                                "outcome": "unverified",
                                "error": "timeout" if kind == "TIMEOUT" else str(e),
                                "attempts": attempt,
                                "elapsed_seconds": round(elapsed, 2)})
                unverified_count += 1
                unverified_items.append(
                    (i, item.get("post_name"), f"{kind} after {elapsed:.0f}s"))
                break

            except Exception as e:
                elapsed = (datetime.now() - start_time).total_seconds()
                log(f"ERROR: Item {i}/{total} after {elapsed:.2f}s: {type(e).__name__}: {e}")
                log(traceback.format_exc())
                results.append({"item_index": i, "error": str(e), "elapsed_seconds": round(elapsed, 2)})
                fail_count += 1
                failed_items.append((i, [f"{type(e).__name__}: {e}"]))
                break

    total_elapsed = (datetime.now() - overall_start).total_seconds()
    log("=" * 60)
    log(f"All items processed. PUBLISHED: {success_count}, FAILED: {fail_count}, "
        f"UNVERIFIED: {unverified_count}, Total time: {total_elapsed:.2f}s")
    for idx, errs in failed_items:
        log(f"  -> item {idx} FAILED: {'; '.join(errs)}")
    for idx, name, why in unverified_items:
        log(f"  -> item {idx} UNVERIFIED ({name}): {why} — may already be live, "
            f"VERIFY before re-sending")

    output_file = f"post_{today}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"Results saved to '{output_file}'")
    log("Script completed.")
    log("=" * 60)
    # Non-zero exit when ANY item failed to publish, so the caller can branch on it
    # and raise the Slack alert instead of reading a misleading success line.
    # Both states need a human, but they mean different things: FAILED is a real
    # rejection and is safe to re-send; UNVERIFIED must be checked first or the
    # re-send duplicates a post that is already live.
    if fail_count or unverified_count:
        sys.exit(2)


if __name__ == "__main__":
    main()