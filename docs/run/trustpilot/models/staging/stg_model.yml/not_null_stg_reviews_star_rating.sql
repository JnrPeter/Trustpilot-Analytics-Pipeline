
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select star_rating
from TRUSTPILOT_REVIEWS.DEV.stg_reviews
where star_rating is null



  
  
      
    ) dbt_internal_test