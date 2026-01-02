{# 
    Test: 
    Checks for duplicate reviews in raw source data. 
    We do this by using the columns we are going to use to generate the surrogate key(review_id) to check
    Result: Returns rows where the same review appears more than once.
#}

select 
    company_name,
    reviewer_name,
    review_date,
    review_title,
    review_text,
    count(*) as duplicate_count
from {{ source('trustpilot', 'reviews') }}
group by 1, 2, 3, 4, 5
having count(*) > 1