






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and overall_rating >= 1 and overall_rating <= 5
)
 as expression


    from TRUSTPILOT_REVIEWS.DEV.stg_profile
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







