
  
    

create or replace transient table TRUSTPILOT_REVIEWS.DEV.dim_company_profile
    
    
    
    as (with companies as (
    select * from TRUSTPILOT_REVIEWS.DEV.stg_profile
),

final as (
    select
        -- Primary key
        company_id,
        
        -- Attributes
        company_name,
        business_type,
        trustpilot_url,
        website_url,
        phone,
        
        -- Ratings
        overall_rating,
        trust_category,
        
        -- Rating tier for grouping
        case
            when overall_rating >= 4.5 then 'Excellent'
            when overall_rating >= 4.0 then 'Good'
            when overall_rating >= 3.0 then 'Average'
            else 'Poor'
        end as rating_tier,
        
        -- Review metrics
        total_reviews,
        
        -- Location metrics
        num_locations,
                CASE
                WHEN num_locations = 1 THEN 'Single'
                WHEN num_locations BETWEEN 2 AND 10 THEN 'Regional'
                ELSE 'National'
            END AS company_size,
        
        -- Response metrics
        negative_response_pct,
        response_time_hours,
        
        -- Response tier for grouping
        case
            when response_time_hours is null then 'Unknown'
            when response_time_hours <= 24 then 'Fast'
            when response_time_hours <= 72 then 'Moderate'
            else 'Slow'
        end as response_tier,
        
        -- Responsive flag (replies to 50%+ of negative reviews)
        case
            when negative_response_pct >= 50 then true
            else false
        end as is_responsive,
        
        -- Profile status
        claimed_profile,
        verified_company,
        has_active_subscription,
        
        -- Metadata
        scraped_at

    from companies
)

select * from final
    )
;


  