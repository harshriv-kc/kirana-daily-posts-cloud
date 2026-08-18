# Patch request: `idempotency_key` for `postAutomation`

**Repo:** `Hogwarts-CloudSpells` → `UTILITY/postAutomation`
**Asked for by:** kirana-daily-posts routine (`harshriv-kc/kirana-daily-posts-cloud`)
**Why now:** on 2026-08-18 this cost us 3 duplicate posts and duplicate push
notifications to real users.

---

## The problem in one paragraph

`postAutomation` does all its work inside a single synchronous HTTP request:
generate 1–2 Gemini images, POST to the News API, write `news_generation_logs`,
then answer. Heavy posts take 120–300+s. Our connection to the function is cut at
~300s, and Cloud Functions does **not** abort when the caller disconnects — so the
function finishes and the post IS created, but the caller never receives the
`post_id`. The caller cannot distinguish "created" from "not created", so it must
choose between **skipping a real post** or **publishing a duplicate**. Both are bad.
There is currently no dedupe anywhere in the handler, so a re-send always creates a
second post and fires a second PN at every user.

The same thing happens one layer deeper: when the function's own call to the News
API loses its response, the error it reports has no status and reads
`API Error: undefined - undefined: undefined`, while the News API may still have
created the post.

## What we need

Accept an optional `idempotency_key` per post. If a **successful** log row already
exists for that key, do not do the work again — return the original result.

That single change makes the caller able to retry safely until it gets a receipt,
which turns "post >300s" from a coin-flip into a guarantee.

## Suggested implementation

### 1. Accept the field

`src/types/interfaces.ts`

```ts
export interface PostRequest {
  post_name: string;
  post_title: string;
  post_description: string;
  commodity?: string;
  direction?: "Teji" | "Mandi" | "Sthir";
  brand_names: string[];
  image_prompt?: string;
  pn_image_prompt?: string;
  notification_title?: string;
  notification_description?: string;
  bg_color?: string;
  idempotency_key?: string;   // <-- add
}
```

### 2. Persist it

Add a column and a **unique index** — the index is what makes this correct under
concurrent/duplicate requests, not just the SELECT:

```sql
ALTER TABLE news_generation_logs
  ADD COLUMN idempotency_key VARCHAR(191) NULL,
  ADD UNIQUE KEY uniq_idem_success (idempotency_key, success);
```

Include it in the `saveLog` INSERT in `src/services/database.service.ts`.

### 3. Short-circuit before doing any work

In `src/index.ts`, before image generation (i.e. before the current Step 1) for
each post:

```ts
if (postRequest.idempotency_key) {
  const existing = await databaseService.findSuccessfulLogByKey(
    postRequest.idempotency_key
  );
  if (existing) {
    const postId = existing.news_api_response?.data?.results?.news?.id ?? null;
    console.log(
      `[idempotency] ${postRequest.idempotency_key} already succeeded, ` +
      `returning existing post ${postId} without regenerating`
    );
    return {
      post_name: postData.post_name,
      success: true,
      post_id: postId,
      d2r_link: postId
        ? `https://d2r.retailpulse.ai/dashboard/article/view/${postId}`
        : null,
      deduplicated: true,          // so the caller can tell it was a replay
    };
  }
}
```

with, in `database.service.ts`:

```ts
async findSuccessfulLogByKey(key: string): Promise<DatabaseLog | null> {
  const [rows] = await this.getPool().execute<RowDataPacket[]>(
    `SELECT * FROM news_generation_logs
      WHERE idempotency_key = ? AND success = 1
      ORDER BY id DESC LIMIT 1`,
    [key]
  );
  return (rows[0] as DatabaseLog) ?? null;
}
```

**Important:** the check must sit before image generation, otherwise a replay still
burns a Gemini call and several minutes.

### 4. Key format we will send

`<posting_date>:<post_name>` — stable for a given day and post, e.g.

```
2026-08-18:सोया तेल
2026-08-18:Samachar
```

Stable across retries of the same run, and different every day, which is exactly
the dedupe window we want. If you prefer an opaque key, any per-post UUID the
caller generates once and reuses across retries works equally well — just say so
and we will send that instead.

## How we will use it

`post_items.py` sends the key on every post and, once you confirm this is live, we
flip `BACKEND_SUPPORTS_IDEMPOTENCY = True`. From then on the poster retries any
lost response until it gets a receipt, because a replay can no longer create a
second post. Until then the poster refuses to retry at all and reports those items
as UNVERIFIED for a human to check.

## Please also consider (bigger, optional)

Making the endpoint async would remove this failure class entirely rather than make
it survivable: return `202 + job_id` immediately, do the work in the background, and
add a `GET ?job_id=` status route to poll. A ~14.8 min average behind a synchronous
HTTP call will keep producing this problem for every caller, not just us.

## What we need back

1. Confirmation the field is live, and whether the key format above is fine.
2. Whether `deduplicated: true` (or similar) will be in the response, so our logs
   can distinguish a fresh publish from a replay.
