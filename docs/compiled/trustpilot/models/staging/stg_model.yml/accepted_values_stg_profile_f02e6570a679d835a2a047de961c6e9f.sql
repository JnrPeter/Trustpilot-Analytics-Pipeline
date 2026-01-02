
    
    

with all_values as (

    select
        trust_category as value_field,
        count(*) as n_records

    from TRUSTPILOT_REVIEWS.DEV.stg_profile
    group by trust_category

)

select *
from all_values
where value_field not in (
    'Excellent','Great','Poor','Bad'
)


