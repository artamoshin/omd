WITH posts_scd AS (
    SELECT post_id, views, likes, shares, MIN(dttm) AS effective_from
    FROM posts_stats
    GROUP BY post_id, views, likes, shares
    ORDER BY post_id, effective_from
)

SELECT *,
       COALESCE(LEAD(effective_from) OVER (PARTITION BY post_id), TIMESTAMP '9999-12-31 23:59:59') AS effective_to
FROM posts_scd;