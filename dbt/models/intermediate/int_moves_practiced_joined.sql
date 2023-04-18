with moves_practiced as (
    select * from {{ source("bjj", "moves_practiced") }}
),

move as (
    select * FROM {{ source("bjj", "move") }}
),

joined as (
    select
        date,
        extract(year from date)::text as year,
        class_id,
        move_id,
        m.name AS move
    from moves_practiced mp
    left join move m on mp.move_id = m.id
)

select * from joined
