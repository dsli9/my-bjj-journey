"""bjj_journey.streamlit_app.plots - Create plots for BJJ dashboard app.

"""
from typing import Optional
import pandas as pd
import altair as alt

from bjj_journey.streamlit_app.utils import validate_skill_type


def create_times_practiced_skill_bar_chart(
    data: pd.DataFrame, skill_type: str, top_n: Optional[int] = 999
) -> alt.Chart:
    """
    Create a bar chart displaying the number of times the skills within a skill
    type were practiced.
    """
    validate_skill_type(skill_type)

    y_titled = skill_type.title()
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(
                "num_times_practiced:Q",
                axis=alt.Axis(title="Number of Times Practiced", tickMinStep=1),
            ),
            y=alt.Y(
                f"{skill_type}:N", sort="-x", axis=alt.Axis(ticks=True, title=y_titled)
            ),
            tooltip=[
                alt.Tooltip(f"{skill_type}:N", title=y_titled),
                alt.Tooltip("num_times_practiced:Q", title="Times Practiced"),
            ],
        )
        .transform_window(
            rank="rank(num_times_practiced)",
            sort=[alt.SortField("num_times_practiced", order="descending")],
        )
        .transform_filter((alt.datum.rank < top_n))
    )
    return chart


def create_num_classes_by_month_line_chart(
    data: pd.DataFrame, dashboard_view: str
) -> alt.Chart:
    """Create a line chart displaying the number of classes attended per month.

    If the dashboard view is set to "Overall", the line chart will have multiple
    series, one per year.
    """
    x_encoding = alt.X(
        "month(month):N",
        axis=alt.Axis(title="Month"),
        scale=alt.Scale(domain=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
    )
    y_encoding = alt.Y(
        "num_classes:Q",
        axis=alt.Axis(title="Number of Classes"),
        scale=alt.Scale(domain=[0, 30]),
    )
    color = {} if dashboard_view != "Overall" else "year:N"
    tooltip = [
        alt.Tooltip("year:N", title="Year"),
        alt.Tooltip("month(month):N", title="Month"),
        alt.Tooltip("num_classes:Q", title="Number of Classes"),
    ]

    chart = (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(x=x_encoding, y=y_encoding, color=color, tooltip=tooltip)
        .configure_point(size=50)
    )

    return chart
