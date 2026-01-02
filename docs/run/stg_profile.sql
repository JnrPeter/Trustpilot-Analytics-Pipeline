
  create or replace   view TRUSTPILOT_REVIEWS.DEV.stg_profile
  
   as (
    WITH clean_profiles AS (
    SELECT * 
    FROM TRUSTPILOT_REVIEWS.RAW.COMPANY_PROFILES
)

SELECT 
    md5(cast(coalesce(cast(TRIM(company_name) as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS company_id,
    TRIM(company_name) AS company_name,
    trustpilot_url,
    scraped_at,
    overall_rating,
    TRIM(trust_category) AS trust_category,
    total_reviews,
    claimed_profile,
    num_locations,
    TRIM(business_type) AS business_type,
    website_url,
    verified_company,
    phone,
    has_active_subscription,
    
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

FROM clean_profiles
WHERE company_name IS NOT NULL
  );

