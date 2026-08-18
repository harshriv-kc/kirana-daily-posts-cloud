---
name: kirana-daily-posts
description: >-
  Generate the 8 daily Kirana Club news/commodity social-media posts from the attached
  व्यापार केसरी (VK) Hindi commodity newspaper PDF, output as an API-ready payload.
  ALWAYS use this skill whenever the user asks for "today's posts", gives a date like
  "18 june", "kal ki posts", or uploads a VK / व्यापार केसरी PDF and says things like
  "this", "using this", "generate posts", "make the curl", or "daily kirana". The skill
  produces TWO deliverables every time without being asked: (1) a copy-pastable curl
  .sh file and (2) the same payload as a pretty-printed .json file. Trigger even if the
  user only says a date or only says "json" — they want the full daily run.
---

# Kirana Daily Posts

Produce exactly **8 posts** for the Kirana Club D2R platform from one VK newspaper PDF plus
web research, then emit them as an API-ready array in **two formats**: a curl `.sh` and a
`.json`. The audience is tier-2/3 Indian kirana (grocery) shop owners; everything is read
aloud by an AI anchor and shown as app push notifications, so language must be simple spoken
Hindi.

The authoritative spec lives in the project files:
- `kirana-posts-content.md` — config, content buckets, sources, quality guardrails
- `kirana-posts-format-and-pn.md` — titles, descriptions, push notifications, colour schemes
- `kirana-posts-media-and-api.md` — image_prompt / pn_image_prompt templates, API mapping, validation

This skill is the operational checklist on top of them — read the project files for any edge case
not covered here.

## Always output BOTH formats

Every run ends with two files in `/mnt/user-data/outputs/`:
1. `kirana_posts_<DDmonth>.sh` — the `curl -X POST ... -d '[...]'` command.
2. `kirana_posts_<DDmonth>.json` — the identical post array, `indent=2`, `ensure_ascii=False`.

Do not wait for the user to ask for JSON — they always want it. Present the `.sh` first, then
the `.json`, with one short summary table. No long postamble.

## Auto-save to Google Drive (every run)

After both files are written and validated, upload **both** of them to the user's Google Drive
folder **"Kirana Daily Posts"** (folder ID `1UOxJf1q_4B76ks_h5oxhc20z1jjA7QpE`). This happens on
every run without being asked — it is part of the standard output, same as the local files.

How:
1. The Drive tool is deferred — load it first: `tool_search(query="Google Drive create file")`,
   which exposes `Google Drive:create_file`.
2. Read each output file's text and upload it with `Google Drive:create_file`:
   - `parentId`: `1UOxJf1q_4B76ks_h5oxhc20z1jjA7QpE`
   - `title`: `kirana_posts_<YYYY-MM-DD>.json` and `kirana_posts_<YYYY-MM-DD>.sh` (ISO posting
     date so the folder sorts chronologically, e.g. `kirana_posts_2026-06-18.json`)
   - `textContent`: the file contents
   - `contentMimeType`: `application/json` for the JSON, `text/plain` for the `.sh`
   - `disableConversionToGoogleType`: `true` on both (keep them as raw downloadable files, NOT
     Google Docs/Sheets)
3. Files are **added, never overwritten** — each day keeps its own dated copy.

Connector note: this needs the Google Drive connector to be connected. If `create_file` errors or
the connector is unavailable, do NOT fail the run or invent a workaround — the local `.sh`/`.json`
are still the primary deliverables. Tell the user the Drive upload failed and that the files are in
`/mnt/user-data/outputs/`, and let them decide how to proceed. (The structured `google_drive_search`
endpoint has been flaky; `create_file` is independent of it and is the only Drive call needed here.)

## The n+1 date rule

The VK PDF is dated **one day before** the posting date (it carries a "डाक <date>" stamp = the
posting date). So a paper dated 17 जून → posts for **18 जून**. Confirm by reading the डाक stamp.
Every `post_title` and heading uses the posting date in Hindi format with Arabic numerals:
`18 जून:` (never Devanagari digits, never the event date).

**This is the n+1 case, not a law.** The governing rule is the **latest-paper rule**: always
draft from the newest issue published at run time, whatever its cover date — `run_kirana.py
fetch` picks it and reports `pdf_used` / `gap_days` / `stale_reuse`. In every case the posting
date comes from `fetch`, never from the paper's own cover or डाक date.

**Schedule: 07:00 IST on the posting day, morning only — there is NO evening run.** At 07:00
the same-day issue is already up 96% of the time, so the normal result is `gap_days: 0`
(cover date == posting date). After a Sunday or a publisher skip you get `gap_days: 1+` and
the reuse rule applies.

**⏱ सोया तेल — the first user-visible post — must be live by 08:00 IST.** The pipeline has
one hour. If you slip past 08:00, DM Harsh (`U09K92G1U1X`) straight away with the real
timestamp so he can adjust the visible time by hand; do not wait for the run to finish.

**If `stale_reuse` is true** — either because no paper was published (weekend/holiday) or
because we are early and it is not up yet — **post the full 8 anyway.** Use the previous
day's paper and change the **framing and the images**; **repeated prices are fine and are
not a reason to skip or hedge.** A missing new paper never means a missing post day. Full
rule + precedents: `kirana-posts-content.md` → "WHICH PAPER TO USE — THE LATEST-PAPER RULE".

**If the run fails** (no paper at all, validation stuck, any item fails to publish, or the
ledger push fails): **Slack DM Harsh — `U09K92G1U1X` — and nobody else.** A stale-paper
reuse day is NOT a failure and gets no DM. See `kirana-posts-content.md` → "FAILURE ALERTS".

**⛔ Never re-send an UNVERIFIED item.** `post_items.py` reports three outcomes:
PUBLISHED, FAILED (backend rejected it — safe to re-send) and UNVERIFIED (connection
died before the reply arrived). `postAutomation` keeps running after we disconnect, so
an UNVERIFIED post is **probably already live with its push notification delivered**.
Re-sending it duplicates the post AND fires a second PN at every user — this happened
on 2026-08-18 because the run called them "failed". Report the three buckets separately
and leave UNVERIFIED items for a human to check. Full rule: `kirana-posts-content.md`
→ "FAILED vs UNVERIFIED".

## Workflow

1. **Read the VK PDF** (in `/mnt/user-data/uploads/`). It is in context as an image/PDF — decode
   prices directly. `pdftotext` output is usually garbled; use it only as a cross-check. Extract
   every commodity, exact price, change (↑/↓), reason, and outlook. Commodity data comes ONLY
   from the PDF — never web-search prices.
2. **Avoid repetition (read the ledger).** Read `kirana-used-log.json` (autopilot) or use
   `conversation_search` / `recent_chats` (manual runs). Today must differ on every axis: Samachar
   hero, oil direction, dal, Other pick, rujhan quiz commodity, the scheme, and **both trending
   themes**. For trending, build the set of `trending_1_theme`/`trending_2_theme` used in the last
   **7 days** and treat any evergreen theme there (scam, monsoon-weather, fmcg-price, etc.) as
   BANNED today — compare by THEME tag, not topic sentence (monsoon-arriving = monsoon-drought).
3. **Web-search** ONLY for: Trending News 1 & 2 and the Scheme. **No hard "TN1 = fraud" rule and
   neither trending post has to be a scheme.** Search the full theme pool, apply the 7-day theme
   cooldown, then pick the **2 most relevant** (rank by relevance + click data); the two must be
   different themes and unrelated, lean net-positive, and rotate so all themes appear over ~2–3
   weeks. GST normally skipped — rare ground-breaking change only, explained from scratch. Excluded
   always: quick-commerce, app/tech-company, stock-market. See `field-rules.md` + `kirana-posts-content.md`
   §4 for the full pool, selection logic, GST rule, and avoid-list.
4. **Draft all 8 posts** per `references/field-rules.md` (post lineup, HTML formats, PN 3-line
   logic, image_prompt / pn_image_prompt rules, colour schemes, Rujhan VAR rotation).
5. **Build & validate & emit** with `scripts/emit_posts.py` — pass it the 8 post dicts; it writes
   both files and runs the full validation. Fix anything it flags before presenting.
6. **Auto-save to Google Drive** — upload both files to the "Kirana Daily Posts" folder per the
   "Auto-save to Google Drive" section above. Standard on every run.

## Validation (the script enforces these)

- Exactly 8 posts; body is a JSON array `[ {...} ]`.
- 8 unique `bg_color`s = 5 light + 3 dark (darks: `#461B83`, `#6D370F`, `#114883`), assigned
  non-sequentially.
- `image_prompt` on ALL 8 posts (Samachar, सोया तेल, दाल/शक्कर, Other commodities, रुझान,
  Trending News 1, Trending News 2, Schemes).
- `pn_image_prompt` ONLY on: Samachar, दाल/शक्कर, रुझान, Trending News 1, Trending News 2.
- `commodity` + `direction` ONLY on: सोया तेल, दाल/शक्कर, Other commodities, रुझान.
- `brand_names` (array, `[]` allowed) + `bg_color` on all 8.
- Every title starts with the posting date (`18 जून`). No `$` anywhere (spell "डॉलर"). No
  citation markers / source names. **No ASCII apostrophes anywhere** (they break the single-quoted
  shell payload). All Hindi sentences end with `।`. No duplicate emoji within a single PN. The
  Samachar PN commodity must differ from the four commodity-post PNs.

## Post names (exact values) — and the ORDER they must be written in

**`सोया तेल` MUST be the first object in the array.** It is the first post users see
(08:00 IST), and the poster sends items in array order, so putting it first means it
clears the 8 AM slot a few minutes into the run even if the rest run long. Write the 8
in exactly this order:

1. `सोया तेल`  ← first, deadline-critical
2. `Samachar`
3. `दाल/शक्कर`
4. `Other commodities`
5. `रुझान`
6. `Pan India Trending News 1`
7. `Pan India Trending News 2`
8. `Pan India Schemes`

Read `references/field-rules.md` before drafting — it holds the detailed per-post templates,
colour table, PN patterns, and the Rujhan pn_image VAR rotation (date mod 4).
