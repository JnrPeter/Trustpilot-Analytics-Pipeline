
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select company_name
from TRUSTPILOT_REVIEWS.DEV.stg_reviews
where company_name is null



  
  
      
    ) dbt_internal_test