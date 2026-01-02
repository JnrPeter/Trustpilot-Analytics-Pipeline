
with clean_reviews_one as (
    select * 
    from TRUSTPILOT_REVIEWS.RAW.REVIEWS
),

clean_reviews_without_duplicates as (
    select 
        *,
        row_number() over (
            partition by company_name, reviewer_name, review_date, review_title, review_text
            order by scraped_at desc
        ) as row_num
    from clean_reviews_one
),

final_cleaned as (
    select
        -- Primary key
        md5(cast(coalesce(cast(TRIM(company_name) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(reviewer_name as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(review_date as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(review_title as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(review_text as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as review_id,
        
        -- Foreign key
        md5(cast(coalesce(cast(TRIM(company_name) as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as company_id,
        
        -- Company
        trim(company_name) as company_name,
        
        -- Reviewer
        trim(reviewer_name) as reviewer_name,
        trim(reviewer_location) as reviewer_location,
        
        -- Rating
        case
            when rating like '%1 out of 5%' then 1
            when rating like '%2 out of 5%' then 2
            when rating like '%3 out of 5%' then 3
            when rating like '%4 out of 5%' then 4
            when rating like '%5 out of 5%' then 5
            else null
        end as star_rating,
        
        -- Review content
        trim(review_title) as review_title,
        trim(review_text) as review_text,
        review_length,
        
        -- Date
        review_date as reviewed_at,
        
        -- Flags
        verified_review as is_verified,
        has_company_reply,
        
        -- Topics
        trim(lower(topic_tags)) as topic_tags,
        
        -- Metadata
        scraped_at

    from clean_reviews_without_duplicates
    where row_num = 1  -- Keep only first occurrence
      and company_name is not null
      and review_date is not null
)

select * from final_cleaned