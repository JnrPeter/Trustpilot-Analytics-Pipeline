select 
    company_name, 
    reviewer_name, 
    review_date, 
    review_title, 
    review_text,
    count(*) as duplicate_count
from TRUSTPILOT_REVIEWS.RAW.REVIEWS
group by company_name, reviewer_name, review_date, review_title, review_text
having count(*) > 1