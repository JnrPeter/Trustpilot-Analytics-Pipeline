
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select review_rating
from TRUSTPILOT_REVIEWS.DEV.fct_reviews
where review_rating is null



  
  
      
    ) dbt_internal_test