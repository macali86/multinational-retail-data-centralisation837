WITH time_diffs AS (
  SELECT
    dt.year,
    EXTRACT(EPOCH FROM (GREATEST(LEAD(dt.timestamp, 1) OVER (PARTITION BY dt.year ORDER BY dt.date_uuid), dt.timestamp) - dt.timestamp)) AS time_diff_seconds
  FROM dim_date_times dt
)
SELECT
  year,
  CONCAT('{"hours": ', FLOOR(AVG(time_diff_seconds) / 3600), ', "minutes": ', FLOOR((AVG(time_diff_seconds) % 3600) / 60), ', "seconds": ', FLOOR((AVG(time_diff_seconds) % 60) / 1), ', "milliseconds": ', ROUND((AVG(time_diff_seconds) % 1) * 1000)) AS actual_time_taken
FROM time_diffs
WHERE time_diff_seconds IS NOT NULL
GROUP BY year
ORDER BY year;


















