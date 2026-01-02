test_1 as (
    select 
        *,
        row_number() over (
            partition by company_name, reviewer_name, review_date, review_title, review_text
            order by scraped_at desc
        ) as row_num
    from TRUSTPILOT_REVIEWS.RAW.REVIEWS
)

SELECT * FROM 
test_1
WHERE row_num > 1