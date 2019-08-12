WITH posts_scd AS (
    SELECT post_id, views, likes, shares, MIN(dttm) AS effective_from
    FROM posts_stats
    GROUP BY post_id, views, likes, shares
    ORDER BY post_id, effective_from
)

SELECT *,
       (SELECT COALESCE(MIN(effective_from), TIMESTAMP '9999-12-31 23:59:59')
        FROM posts_scd sub
        WHERE sub.post_id = posts_scd.post_id
          AND sub.effective_from > posts_scd.effective_from
       ) AS effective_to
FROM posts_scd;