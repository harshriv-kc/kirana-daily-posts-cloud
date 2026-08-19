# Tech ask — `postAutomation` needs an idempotency key (and ideally an item ID up front)

**Raised after:** 2026-08-19, when the Samachar post was published **twice** and
3 of 8 posts came back with no item ID at all.

**Who this is for:** whoever owns
`https://asia-south1-op-d2r.cloudfunctions.net/postAutomation`.

---

## What happened

The daily Kirana routine sends 8 posts, one HTTP request each. The requests run
from a Claude Code cloud sandbox, which reaches the internet through a managed
egress proxy that **severs any request at ~300s**. Measured on 2026-08-19:

| Post | Images generated | Duration | Outcome |
|---|---|---|---|
| सोया तेल | 1 | 120.0s | OK, item ID returned |
| Samachar | 2 | **>300s** | response lost |
| दाल/शक्कर | 2 | **>300s** | response lost |
| Other commodities | 1 | 54.8s | OK |
| रुझान | 2 | 240.8s | OK |
| Trending News 1 | 2 | **>300s** | response lost |
| Trending News 2 | 2 | 213.8s | OK |
| Schemes | 1 | 50.0s | OK |

The four failures landed at 301.00, 300.53, 300.42 and 300.39s — 0.6s of spread.
That is a fixed ceiling, not the backend timing out. Our client asks for 600s.

**The clean correlation: posts carrying a second image (`pn_image_prompt`) take
200–300s+; single-image posts finish in under 120s.** The endpoint generates
images synchronously inside the request, so the 5 two-image posts are the ones
at risk every single day.

## Why it caused a duplicate

A severed response is **ambiguous, not a failure** — the request reached the
backend and the post was created; only the reply was lost. So the caller cannot
tell "created" from "not created", and has no item ID either way.

On 19 Aug the poster was resumed and re-sent Samachar. Both sends had in fact
succeeded → two posts, two push notifications to every user.

We have since made the client strictly at-most-once (an item that was ever
attempted is never re-sent automatically). That stops duplicates, but it means
**any post whose response is lost simply does not go out**, and needs a human to
eyeball the feed. That is not a good steady state: on 19 Aug it would have left
3 of 8 posts in limbo.

---

## The ask — any ONE of these fixes it. Ranked by effort.

### 1. Accept an `idempotency_key` (smallest change, strongly preferred)

Let the request carry a caller-supplied key, stable per post per day:

```json
{ "idempotency_key": "kirana-2026-08-19-samachar", "post_name": "Samachar", ... }
```

Behaviour: if a post with that key already exists, **do not create a second
one — return the existing `itemId` and `d2r_link` with HTTP 200.**

This solves both problems at once:
- a duplicate becomes impossible even if we retry;
- a lost response is recovered by simply re-sending and reading back the
  existing item ID.

Storage is one indexed column. This is the change we would like most.

### 2. Return the item ID immediately, generate images asynchronously

Respond `202 Accepted` with `{ "itemId": "...", "d2r_link": "..." }` as soon as
the record is created (sub-second), and do image generation in the background.
Optionally expose `GET /postAutomation/status?itemId=…` so we can confirm the
images landed.

No request would ever approach 300s again, and every response carries an ID.

### 3. Expose a lookup

`GET /postAutomation?date=2026-08-19&post_name=Samachar` → `itemId` /
`d2r_link` / `not_found`.

Lets the caller reconcile a lost response without ever re-sending blind. Weakest
of the three (it is a workaround, not a fix) but unblocks us.

---

## What we have already done on our side

- `post_items.py` is now strictly **at-most-once**: the attempt is written and
  fsynced to a per-day ledger *before* the request goes out, so a lost response,
  a crash, or a re-run can never produce a second send. Re-sending requires an
  explicit human `--force` after checking the feed.
- Every item ID is persisted the instant it arrives (previously results were
  only written after all 8 finished, so a killed process lost them).
- The poster always runs detached so it cannot be truncated mid-run.

None of that can recover an item ID the backend never got to send us. That part
needs one of the three changes above.

**Contact:** design@retailpulse.ai
