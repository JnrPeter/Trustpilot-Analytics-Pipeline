__dbt__cte__test_connection as (


-- models/staging/test_connection.sql
SELECT * FROM TRUSTPILOT_REVIEWS.RAW.REVIEWS LIMIT 10
)