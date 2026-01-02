
    
    

with child as (
    select company_id as from_field
    from TRUSTPILOT_REVIEWS.DEV.stg_reviews
    where company_id is not null
),

parent as (
    select company_id as to_field
    from TRUSTPILOT_REVIEWS.DEV.stg_profile
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


