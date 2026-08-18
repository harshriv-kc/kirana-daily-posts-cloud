import json
import requests
from datetime import datetime
import sys
import time
import os
import traceback


API_URL = "https://asia-south1-op-d2r.cloudfunctions.net/postAutomation"
INPUT_FILE = "request_body.json"

# The cloud runner's egress proxy closes an idle tunnel at ~300s, while the
# backend legitimately takes 120-300s per item (it generates 1-2 images). When
# it overruns, requests raises ConnectionError/ProxyError — NOT Timeout, so the
# `timeout=` below is irrelevant to that failure and raising it does nothing.
# Observed 2026-08-18: items answering in 118-253s all published; three that
# crossed 300s were cut (300.53s, 300.43s, 300.62s) and published fine on a
# manual re-send at 273s, 182s and 165s. Retrying is the only lever.
#
# CAUTION: a dropped connection means the response was LOST, not refused — the
# backend may already have created the post, so a retry can produce a DUPLICATE.
# That is why this is capped low and every retry is logged loudly. Transport
# failures only: a 200 carrying success=false is a real rejection and is never
# retried here.
CONNECTION_RETRIES = 2          # extra attempts after the first
RETRY_BACKOFF_SECONDS = 15      # doubles each attempt: 15s, 30s


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
                item_errors = []
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

                if item_errors:
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

                log(f"FAILED: Item {i}/{total} did NOT publish — {kind} after "
                    f"{attempt} attempt(s)")
                results.append({"item_index": i,
                                "error": "timeout" if kind == "TIMEOUT" else str(e),
                                "attempts": attempt,
                                "elapsed_seconds": round(elapsed, 2)})
                fail_count += 1
                failed_items.append((i, [f"{kind} after {attempt} attempt(s)"]))
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
        f"Total time: {total_elapsed:.2f}s")
    for idx, errs in failed_items:
        log(f"  -> item {idx} FAILED: {'; '.join(errs)}")

    output_file = f"post_{today}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"Results saved to '{output_file}'")
    log("Script completed.")
    log("=" * 60)
    # Non-zero exit when ANY item failed to publish, so the caller can branch on it
    # and raise the Slack alert instead of reading a misleading success line.
    if fail_count:
        sys.exit(2)


if __name__ == "__main__":
    main()