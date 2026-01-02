{#
    Data validation: Confirms that Raw rows - Duplicate rows = Staged rows

#}

with raw_count as (
    select count(*) as rc from {{ source('trustpilot', 'reviews') }}
),

staged_count as (
    select count(*) as sc from {{ ref('stg_reviews') }}
),

duplicate_rows as (
    select count(*) as dr
    from (
        select row_number() over (
            partition by company_name, reviewer_name, review_date, review_title, review_text
            order by scraped_at desc
        ) as row_num
        from {{ source('trustpilot', 'reviews') }}
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
