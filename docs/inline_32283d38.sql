select * from (
WITH clean_reviews AS (
    SELECT * 
    FROM {{ source('trustpilot', 'profile') }}
)

SELECT 
    {{ dbt_utils.generate_surrogate_key(['TRIM(company_name)']) }} AS company_id,
    TRIM(company_name) AS company_name,
    trustpilot_url,
    scraped_at,
    overall_rating,
    TRIM(trust_category) as trust_category ,
    total_reviews,
    claimed_profile,
    num_locations,
    TRIM(business_type) as business_type ,
    website_url,
    verified_company,
    phone,
    has_active_subscription,
    
    -- Transformed columns
    CASE 
        WHEN negative_response_rate = 'Unknown' THEN 0
        ELSE REPLACE(negative_response_rate, '%', '')::NUMERIC
    END AS negative_response_pct,
    
    CASE
        WHEN response_time = 'Unknown' THEN NULL
        WHEN response_time ILIKE '%week%' THEN 
            REGEXP_SUBSTR(response_time, '\\d+')::NUMERIC * 168  
        WHEN response_time ILIKE '%day%' THEN 
            REGEXP_SUBSTR(response_time, '\\d+')::NUMERIC * 24
        WHEN response_time ILIKE '%hour%' THEN 
            REGEXP_SUBSTR(response_time, '\\d+')::NUMERIC
        ELSE NULL
    END AS response_time_hours
FROM clean_reviews
WHERE company_name IS NOT NULL

) as __preview_sbq__ limit 1000