{#
    Fact table for Trustpilot reviews.
    
#}

with reviews as (
    select * from {{ ref('stg_reviews') }}
),

countries as (
    select * from {{ ref('country_codes') }}
),

final as (
    select
        -- Primary key
        review_id,
        
        -- Foreign key
        company_id,
        
        -- Denormalized for convenience
        company_name,
        
        -- Reviewer info
        reviewer_name,
        countries.country_name as reviewer_country,
        
        -- Rating
        star_rating as review_rating,
        
        -- Sentiment flags
        case 
        WHEN star_rating >= 4 THEN 'Positive'
        WHEN star_rating <= 2 then 'Negative'
        WHEN star_rating = 3 THEN 'Neutral'
        END AS review_sentiment,
        
        -- Review content
        review_title,
        review_text,
        review_length,
        
        -- Review length tier
        case
            when review_length < 100 then 'Short'
            when review_length <= 300 then 'Medium'
            else 'Long'
        end as review_length_tier,
        
        -- Dates
        reviewed_at,
        datediff(day, reviewed_at, current_date) as review_age_days,
        
        -- Flags
        is_verified,
        has_company_reply,
        
        -- Topics
        topic_tags,
        case 
            when topic_tags = 'general' or topic_tags is null then 0
            else array_size(split(topic_tags, ', '))
        end as topic_count,
        
        -- Metadata
        reviews.scraped_at

    from reviews
    left join countries
        on reviews.reviewer_location = countries.country_code
)

select * from final