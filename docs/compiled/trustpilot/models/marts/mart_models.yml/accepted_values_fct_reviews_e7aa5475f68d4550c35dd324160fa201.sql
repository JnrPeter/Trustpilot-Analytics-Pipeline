
    
    

with all_values as (

    select
        review_length_tier as value_field,
        count(*) as n_records

    from TRUSTPILOT_REVIEWS.DEV.fct_reviews
    group by review_length_tier

)

select *
from all_values
where value_field not in (
    'Short','Medium','Long'
)


