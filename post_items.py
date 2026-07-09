import json
import requests
from datetime import datetime
import sys
import os
import traceback


API_URL = "https://asia-south1-op-d2r.cloudfunctions.net/postAutomation"
INPUT_FILE = "request_body.json"


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
    fail_count = 0
    overall_start = datetime.now()

    for i, item in enumerate(request_body, start=1):
        log(f"--- Sending item {i}/{total} ---")
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
                "elapsed_seconds": round(elapsed, 2),
                "response": resp_data,
            })

            if response.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
                log(f"WARNING: Item {i} returned non-200 status: {response.status_code}")

        except requests.exceptions.Timeout:
            elapsed = (datetime.now() - start_time).total_seconds()
            log(f"TIMEOUT: Item {i}/{total} timed out after {elapsed:.2f}s")
            results.append({"item_index": i, "error": "timeout", "elapsed_seconds": round(elapsed, 2)})
            fail_count += 1

        except requests.exceptions.ConnectionError as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            log(f"CONNECTION ERROR: Item {i}/{total} after {elapsed:.2f}s: {e}")
            log(traceback.format_exc())
            results.append({"item_index": i, "error": str(e), "elapsed_seconds": round(elapsed, 2)})
            fail_count += 1

        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            log(f"ERROR: Item {i}/{total} after {elapsed:.2f}s: {type(e).__name__}: {e}")
            log(traceback.format_exc())
            results.append({"item_index": i, "error": str(e), "elapsed_seconds": round(elapsed, 2)})
            fail_count += 1

    total_elapsed = (datetime.now() - overall_start).total_seconds()
    log("=" * 60)
    log(f"All items processed. Success: {success_count}, Failed: {fail_count}, Total time: {total_elapsed:.2f}s")

    output_file = f"post_{today}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"Results saved to '{output_file}'")
    log("Script completed.")
    log("=" * 60)


if __name__ == "__main__":
    main()