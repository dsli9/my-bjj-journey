with moves_practiced as (
    select * from {{ ref("int_moves_practiced_joined") }}
),

times_practiced_by_month as (
    select
        move,
        'year' as aggregation_category,
        year as aggregation_value,
        'num_times_practiced' as metric_name,
        count(*) AS metric_value
    from moves_practiced
    group by move, aggregation_category, aggregation_value, metric_name
),

times_practiced_overall as (
    select
        move,
        'overall' as aggregation_category,
        'overall' as aggregation_value,
        'num_times_practiced' as metric_name,
        count(*) AS metric_value
    from moves_practiced
    group by move, aggregation_category, aggregation_value, metric_name
),

final as (
    select * from times_practiced_overall
    union
    select * from times_practiced_by_month
)

select
    move,
    metric_name,
    aggregation_category,
    aggregation_value,
    metric_value
from final
