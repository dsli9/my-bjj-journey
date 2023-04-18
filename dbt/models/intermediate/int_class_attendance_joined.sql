with class_attendance as (
    select * from {{ source("bjj", "class_attendance") }}
),

class as (
    select * FROM {{ source("bjj", "class") }}
),

joined as (
    select
        date,
        extract(year from date)::text as year,
        to_char(date, 'YYYY-MM') as month,
        class_id,
        name as class,
        type as class_type,
        duration as class_duration
    from class_attendance ca
    left join class c on ca.class_id = c.id
)

select * from joined
