with positions_practiced as (
    select * from {{ source("bjj", "positions_practiced") }}
),

position as (
    select * FROM {{ source("bjj", "position") }}
),

joined as (
    select
        date,
        extract(year from date)::text as year,
        class_id,
        position_id,
        p.name AS position
    from positions_practiced pp
    left join position p on pp.position_id = p.id
)

select * from joined
