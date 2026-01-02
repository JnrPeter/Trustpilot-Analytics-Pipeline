
    
    

select
    company_id as unique_field,
    count(*) as n_records

from TRUSTPILOT_REVIEWS.DEV.stg_profile
where company_id is not null
group by company_id
having count(*) > 1


