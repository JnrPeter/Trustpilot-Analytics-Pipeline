
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  

with raw_count as (
    select count(*) as rc from TRUSTPILOT_REVIEWS.RAW.REVIEWS
),

staged_count as (
    select count(*) as sc from TRUSTPILOT_REVIEWS.DEV.stg_reviews
),

duplicate_rows as (
    select count(*) as dr
    from (
        select row_number() over (
            partition by company_name, reviewer_name, review_date, review_title, review_text
            order by scraped_at desc
        ) as row_num
        from TRUSTPILOT_REVIEWS.RAW.REVIEWS
    )
    where row_num > 1
)

SELECT 
    r.rc AS raw_count,
    d.dr AS duplicate_rows,
    s.sc AS staged_count
FROM raw_count r,
     staged_count s,
     duplicate_rows d
WHERE r.rc - d.dr != s.sc
  
  
      
    ) dbt_internal_test