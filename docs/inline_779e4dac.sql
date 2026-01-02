select * from (
WITH clean_profiles AS (
    SELECT * 
    FROM {{ source('trustpilot', 'profile') }}
)
) as __preview_sbq__ limit 1000