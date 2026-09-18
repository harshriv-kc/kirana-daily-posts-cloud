-- Reconcile a day's Kirana post IMAGES against what actually got generated.
-- Database: main (via Birbal query_db).
--
-- WHY THIS EXISTS
-- postAutomation SWALLOWS image failures by design. In
-- Hogwarts-CloudSpells/UTILITY/postAutomation/src/index.ts the image block ends:
--
--     } catch (imageError) {
--       ... saveImageGenerationLog(...)   // failure recorded HERE, nowhere else
--       // Continue with default attachment instead of failing the entire post
--     }
--
-- So the post still publishes, the response is {"success": true}, and
-- post_items.py correctly reports PUBLISHED. The poster CANNOT see a failed
-- image. image_generation_logs is the only record.
--
-- This went unnoticed for weeks: 9 of the 15 days from 2026-09-04 to 2026-09-18
-- shipped at least one post with a placeholder thumbnail (10 failures total,
-- Pan India Trending News 2 six times) and not one run ever reported it.
-- Found 2026-09-18 only because the operator spotted रुझान in the feed.
--
-- RUN THIS AFTER EVERY POSTER RUN (STEP 8c), before the Slack asset-links
-- message. Any row query 1 returns, or any post query 2 lists, is a FAILURE
-- that must be named in the report, marked in the Slack message, and DM'd to
-- Harsh (U09K92G1U1X).
--
-- Set the date on every WHERE clause below to the posting date.

-- 1) Hard failures: an image generation that errored out.
--    generation_type NULL = the post thumbnail (image_prompt).
--    generation_type pn_expanded / pn_collapsed = the PN duo images.
SELECT id,
       timestamp,
       post_name,
       IFNULL(generation_type, 'post_thumbnail') AS image_kind,
       error
FROM image_generation_logs
WHERE timestamp >= '2026-09-18 00:00:00'
  AND timestamp <  '2026-09-19 00:00:00'
  AND success = 0
ORDER BY timestamp;

-- 2) Silent duo-image misses: the five posts carrying a pn_image_prompt
--    (Samachar, दाल/शक्कर, रुझान, TN1, TN2) must each produce BOTH a
--    pn_expanded and a pn_collapsed row. The duo block only writes its log
--    rows on the SUCCESS path, so a duo failure leaves NO row at all —
--    absence is the only signal. Anything listed here is a failure.
SELECT expected.post_name,
       SUM(l.generation_type = 'pn_expanded')  AS has_expanded,
       SUM(l.generation_type = 'pn_collapsed') AS has_collapsed
FROM (
       SELECT 'Samachar' AS post_name
  UNION SELECT 'दाल/शक्कर'
  UNION SELECT 'रुझान'
  UNION SELECT 'Pan India Trending News 1'
  UNION SELECT 'Pan India Trending News 2'
) expected
LEFT JOIN image_generation_logs l
       ON l.post_name = expected.post_name
      AND l.success = 1
      AND l.generation_type IN ('pn_expanded','pn_collapsed')
      AND l.timestamp >= '2026-09-18 00:00:00'
      AND l.timestamp <  '2026-09-19 00:00:00'
GROUP BY expected.post_name
HAVING has_expanded IS NULL OR has_expanded = 0
    OR has_collapsed IS NULL OR has_collapsed = 0;

-- 3) Full day's picture — every attempt, for the run report.
SELECT post_name,
       IFNULL(generation_type, 'post_thumbnail') AS image_kind,
       success,
       LEFT(IFNULL(error, ''), 200) AS error
FROM image_generation_logs
WHERE timestamp >= '2026-09-18 00:00:00'
  AND timestamp <  '2026-09-19 00:00:00'
ORDER BY timestamp;

-- CROSS-CHECK against the poster's own output (post_<date>.json):
-- expanded_image_url / collapsed_image_url come from postAutomation's
-- duoImageResult, which is spread into the response ONLY when the duo images
-- succeeded. So for the FIVE pn_image_prompt posts, missing exp/col in
-- post_<date>.json IS a failure signal and must never be waved off.
-- The three posts WITHOUT a pn_image_prompt — सोया तेल, Other commodities,
-- Pan India Schemes — legitimately return no image URLs. That, and only that,
-- is the "some posts return no image URLs, this is normal" case in STEP 9b.
