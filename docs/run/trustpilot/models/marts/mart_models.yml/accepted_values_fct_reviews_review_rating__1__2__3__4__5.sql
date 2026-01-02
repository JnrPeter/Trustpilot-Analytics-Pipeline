
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        review_rating as value_field,
        count(*) as n_records

    from TRUSTPILOT_REVIEWS.DEV.fct_reviews
    group by review_rating

)

select *
from all_values
where value_field not in (
    '1','2','3','4','5'
)



  
  
      
    ) dbt_internal_test