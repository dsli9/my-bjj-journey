with positions_practiced as (
    select * from {{ ref("int_positions_practiced_joined") }}
),

times_practiced_by_month as (
    select
        position,
        'year' as aggregation_category,
        year as aggregation_value,
        'num_times_practiced' as metric_name,
        count(*) AS metric_value
    from positions_practiced
    group by position, aggregation_category, aggregation_value, metric_name
),

times_practiced_overall as (
    select
        position,
        'overall' as aggregation_category,
        'overall' as aggregation_value,
        'num_times_practiced' as metric_name,
        count(*) AS metric_value
    from positions_practiced
    group by position, aggregation_category, aggregation_value, metric_name
),

final as (
    select * from times_practiced_overall
    union
    select * from times_practiced_by_month
)

select
    position,
    metric_name,
    aggregation_category,
    aggregation_value,
    metric_value
from final
