# kirana-daily-posts (cloud)

Daily pipeline that generates the 8 Kirana Club news/commodity posts from the
व्यापार केसरी (VK) newspaper and publishes them via the `postAutomation` API.
Runs as a scheduled **Claude Code cloud routine** (~7:32 PM IST daily) — no laptop required.

## Layout
```
run_kirana.py              fetch newest VK PDF + decide posting_date (reads the ledger)
post_items.py              the poster — POSTs request_body.json items to postAutomation
emit_posts.py              validate() the 8-post array before posting
kirana-used-log.json       ⭐ THE LEDGER — dedup + posting-date state (source of truth)
specs/                     drafting rules the routine reads each run
  SKILL.md                 operational checklist
  kirana-posts-content.md  config, content buckets, sources, §4 trending pool
  field-rules.md           per-post templates, colour table, PN patterns, Rujhan VAR
  kirana-posts-format-and-pn.md
  kirana-posts-media-and-api.md   image_prompt/pn_image_prompt templates + API mapping
```
Runtime artifacts (`pdfs/`, `request_body.json`, `post_*.json/.log`) are git-ignored.

## The ledger is the whole point
`kirana-used-log.json` is mutable state: `run_kirana.py fetch` reads it to pick the
posting date, and every run appends its picks (heroes, oil direction, both trending
`*_theme` tags, scheme, …) newest-first. A 7-day theme cooldown reads it to stop
repeat scam/monsoon. **The routine must commit the updated ledger back to this repo at
the end of every run**, or the next day loses its memory and posts repeat.

## Nightly flow (the routine)
1. `pip install -q requests pymupdf`
2. `git pull` (get the latest ledger)
3. `python run_kirana.py fetch` → posting_date + downloads newest VK PDF to `pdfs/`
4. Render the PDF to PNG (PyMuPDF) and vision-read every commodity/price/change
5. Web-search the 2 trending items + the scheme; apply the 7-day theme cooldown
6. Draft all 8 posts per `specs/` (read them first)
7. Write `request_body.json`; validate via `emit_posts.validate`
8. Append today's run to `kirana-used-log.json`
9. `python post_items.py` (poster — final action)
10. `git add kirana-used-log.json && git commit && git push` (persist the ledger)

## Deps
Python 3, `requests`, `pymupdf` (fitz). Network to `vyaparkesari.com` and
`asia-south1-op-d2r.cloudfunctions.net`. No auth header / secrets required.
