import json
import requests
from datetime import datetime
import sys
import os
import traceback


API_URL = "https://asia-south1-op-d2r.cloudfunctions.net/postAutomation"
INPUT_FILE = "request_body.json"

# Response fields that carry a URL we want surfaced in the daily report.
# The postAutomation API returns d2r_link for every post, but image URLs
# (expanded_image_url / collapsed_image_url) ONLY for posts that carry a
# pn_image_prompt (Samachar, दाल/शक्कर, रुझान, TN1, TN2). Posts without a
# pn_image_prompt (सोया तेल, Other commodities, Pan India Schemes) come back
# with a d2r_link only — there is no image URL in the response to print.
LINK_KEYS = ("d2r_link", "expanded_image_url", "collapsed_image_url")


def _collect_links(node, found=None):
    """Recursively pull every LINK_KEYS url out of an API response object."""
    if found is None:
        found = {}
    if isinstance(node, dict):
        for k, v in node.items():
            if k in LINK_KEYS and isinstance(v, str) and v.startswith("http"):
                found.setdefault(k, v)
            else:
                _collect_links(v, found)
    elif isinstance(node, list):
        for x in node:
            _collect_links(x, found)
    return found


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
                "post_name": item.get("post_name"),
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
            results.append({"item_index": i, "post_name": item.get("post_name"), "error": "timeout", "elapsed_seconds": round(elapsed, 2)})
            fail_count += 1

        except requests.exceptions.ConnectionError as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            log(f"CONNECTION ERROR: Item {i}/{total} after {elapsed:.2f}s: {e}")
            log(traceback.format_exc())
            results.append({"item_index": i, "post_name": item.get("post_name"), "error": str(e), "elapsed_seconds": round(elapsed, 2)})
            fail_count += 1

        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            log(f"ERROR: Item {i}/{total} after {elapsed:.2f}s: {type(e).__name__}: {e}")
            log(traceback.format_exc())
            results.append({"item_index": i, "post_name": item.get("post_name"), "error": str(e), "elapsed_seconds": round(elapsed, 2)})
            fail_count += 1

    total_elapsed = (datetime.now() - overall_start).total_seconds()
    log("=" * 60)
    log(f"All items processed. Success: {success_count}, Failed: {fail_count}, Total time: {total_elapsed:.2f}s")

    output_file = f"post_{today}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"Results saved to '{output_file}'")

    # ---- Consolidated LINKS SUMMARY (surfaced in the daily report every run) --
    # Guarantees all d2r links + every image URL the API returned are printed in
    # one clean block and written to post_<date>.links.txt. Items whose response
    # carried no image URL (posts without a pn_image_prompt) are shown explicitly
    # as "(no image URL returned by API)" instead of being silently dropped.
    links_file = f"post_{today}.links.txt"
    summary_lines = ["=" * 60, f"LINKS SUMMARY — {today}", "=" * 60]
    for r in results:
        idx = r.get("item_index")
        name = r.get("post_name") or "<unknown>"
        status = r.get("status_code")
        header = f"Item {idx} [{name}] — status {status}"
        if r.get("error"):
            header += f" — ERROR: {r['error']}"
        summary_lines.append(header)
        links = _collect_links(r.get("response", {}))
        d2r = links.get("d2r_link")
        summary_lines.append(f"  d2r_link : {d2r if d2r else '(none returned)'}")
        exp = links.get("expanded_image_url")
        col = links.get("collapsed_image_url")
        if exp or col:
            if exp:
                summary_lines.append(f"  image (expanded) : {exp}")
            if col:
                summary_lines.append(f"  image (collapsed): {col}")
        else:
            summary_lines.append("  image    : (no image URL returned by API)")
    summary_lines.append("=" * 60)
    summary_text = "\n".join(summary_lines)
    for line in summary_lines:
        log(line)
    with open(links_file, "w", encoding="utf-8") as f:
        f.write(summary_text + "\n")
    log(f"Links summary saved to '{links_file}'")

    log("Script completed.")
    log("=" * 60)


if __name__ == "__main__":
    main()