-- Reconcile a day's Kirana posts against what the backend ACTUALLY created.
-- Database: main (via Birbal query_db).
--
-- WHY THIS EXISTS
-- postAutomation averages ~14.8 min per call, while the sandbox egress proxy
-- severs any request at ~300s. So the poster regularly never sees the response
-- even though the post WAS created. news_generation_logs is written by the
-- cloud function itself, so it is the source of truth -- not the poster's log.
--
-- RUN THIS AFTER EVERY POSTER RUN. It gives you:
--   * the itemID of every post, including ones whose response was lost
--   * live_copies > 1 => a duplicate that must be deleted
--
-- itemID path in the response: $.data.results.news.id
-- `timestamp` is when the request STARTED; `id` is assigned when it FINISHED,
-- so ids can be out of order relative to timestamp on slow items.

-- 1) Per-post summary: how many live copies, and their itemIDs.
SELECT DATE(timestamp)                                              AS post_date,
       JSON_UNQUOTE(JSON_EXTRACT(request_data,'$[0].post_name'))    AS post_name,
       COUNT(*)                                                     AS sends,
       SUM(success = 1)                                             AS live_copies,
       GROUP_CONCAT(CASE WHEN success = 1
            THEN JSON_UNQUOTE(JSON_EXTRACT(news_api_response,'$.data.results.news.id'))
            END ORDER BY timestamp SEPARATOR '  |  ')               AS item_ids,
       GROUP_CONCAT(TIME(timestamp) ORDER BY timestamp SEPARATOR ', ') AS sent_at_utc
FROM news_generation_logs
WHERE timestamp >= '2026-08-19 00:00:00'   -- <-- set to the posting date
GROUP BY post_date, post_name
ORDER BY post_date, MIN(timestamp);

-- 2) Duplicates only: the second and later copies are what you delete.
--    Keep the EARLIEST successful copy of each post; delete the rest.
SELECT post_date, post_name, item_id, sent_at_utc, copy_no,
       CASE WHEN copy_no = 1 THEN 'KEEP' ELSE 'DELETE' END AS action
FROM (
  SELECT DATE(timestamp) AS post_date,
         JSON_UNQUOTE(JSON_EXTRACT(request_data,'$[0].post_name')) AS post_name,
         JSON_UNQUOTE(JSON_EXTRACT(news_api_response,'$.data.results.news.id')) AS item_id,
         TIME(timestamp) AS sent_at_utc,
         ROW_NUMBER() OVER (
           PARTITION BY DATE(timestamp),
                        JSON_UNQUOTE(JSON_EXTRACT(request_data,'$[0].post_name'))
           ORDER BY timestamp
         ) AS copy_no
  FROM news_generation_logs
  WHERE timestamp >= '2026-08-19 00:00:00'  -- <-- set to the posting date
    AND success = 1
) t
WHERE post_name IN (
  SELECT post_name FROM (
    SELECT JSON_UNQUOTE(JSON_EXTRACT(request_data,'$[0].post_name')) AS post_name
    FROM news_generation_logs
    WHERE timestamp >= '2026-08-19 00:00:00' AND success = 1
    GROUP BY 1 HAVING COUNT(*) > 1
  ) d
)
ORDER BY post_date, post_name, copy_no;
