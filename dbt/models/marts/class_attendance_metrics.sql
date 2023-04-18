with class_attendance as (
    select * from {{ ref("int_class_attendance_joined") }}
),

num_class_min_by_year as (
     select
        'year' as aggregation_category,
         year as aggregation_value,
        'num_class_minutes' as metric_name,
        sum(class_duration) AS metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

num_classes_by_year as (
    select
        'year' as aggregation_category,
        year as aggregation_value,
        'num_classes_attended' as metric_name,
        count(*) AS metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

num_classes_by_month as (
    select
        'month' as aggregation_category,
        month as aggregation_value,
        'num_classes_attended' as metric_name,
        count(*) AS metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

num_class_min_by_month as (
    select
        'month' as aggregation_category,
         month as aggregation_value,
        'num_class_minutes' as metric_name,
        sum(class_duration) AS metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

num_classes_overall as (
    select
        'overall' as aggregation_category,
        'overall' as aggregation_value,
        'num_classes_attended' as metric_name,
        count(*) AS metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

num_class_min_overall as (
    select
        'overall' as aggregation_category,
        'overall' as aggregation_value,
        'num_class_minutes' as metric_name,
        sum(class_duration) as metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

num_months_trained_by_year as (
    select
        'year' as aggregation_category,
        year as aggregation_value,
        'num_months_trained' as metric_name,
        count(distinct month) as metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

num_months_trained_overall as (
    select
        'overall' as aggregation_category,
        'overall' as aggregation_value,
        'num_months_trained' as metric_name,
        count(distinct month) as metric_value
    from class_attendance
    group by aggregation_category, aggregation_value, metric_name
),

final as (
    select * from num_class_min_overall
    union
    select * from num_classes_overall
    union
    select * from num_class_min_by_month
    union
    select * from num_classes_by_month
    union
    select * from num_class_min_by_year
    union
    select * from num_classes_by_year
    union
    select * from num_months_trained_by_year
    union
    select * from num_months_trained_overall
)

select metric_name, aggregation_category, aggregation_value, metric_value from final
