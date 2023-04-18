"""streamlit_app.py - Script for creating BJJ dashboard app via Streamlit.

"""
from typing import Final
from dotenv import load_dotenv
import streamlit as st
from bjj_journey.streamlit_app.data import BJJDataFetcher

from bjj_journey.streamlit_app.plots import (
    create_num_classes_by_month_line_chart,
    create_times_practiced_skill_bar_chart,
)
from bjj_journey.streamlit_app.utils import (
    add_vertical_space,
    resolve_most_practiced_headline,
)


load_dotenv()

DATA_FETCHER = BJJDataFetcher()

PAGE_TITLE = "BJJ Dashboard"
APP_TITLE = "BJJ Dashboard"
PAGE_ICON = ":martial_arts_uniform:"
LAYOUT: Final = "wide"
DASHBOARD_VIEW_OPTIONS = ["Overall", "2023", "2022"]

# Set page config
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

# Sidebar
with st.sidebar:
    dashboard_view = st.selectbox(
        label="Dashboard View:", options=DASHBOARD_VIEW_OPTIONS
    )
    st.write(f"Data last updated at {DATA_FETCHER.get_most_recent_update_date()}")
    st.title("About")
    st.info("""
        This is a dashboard displaying data related to my Brazilian jiu-jitsu journey,
        created as a personal project.
        """)
    st.title("Contact")
    st.info("""
        Derek Li

        [LinkedIn](https://www.linkedin.com/in/dereksli/) | [GitHub](https://github.com/dsli9)
        """)


assert dashboard_view  # make mypy happy

# Title the app
st.title(f"{APP_TITLE} ({dashboard_view})")

# Create columns
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)
col6, col7 = st.columns(2)

# Metrics
col1.metric(
    label="Total Time Spent Training",
    value=DATA_FETCHER.get_time_spent_training(dashboard_view),
)
col2.metric(
    label="Total Number of Classes Attended",
    value=DATA_FETCHER.get_number_of_classes_attended(dashboard_view),
)
col3.metric(
    label="Total Class Hours",
    value=DATA_FETCHER.get_total_class_hours(dashboard_view),
)

# Positions Practiced
positions_data = DATA_FETCHER.get_num_times_practiced_skill(
    dashboard_view, skill_type="position"
)
most_practiced_position = DATA_FETCHER.determine_most_practiced_skill(
    positions_data, skill_type="position"
)

with col4:
    st.header("Positions Practiced")
    add_vertical_space(1)
    st.altair_chart(
        altair_chart=create_times_practiced_skill_bar_chart(
            positions_data, skill_type="position"
        ),
        use_container_width=True,
    )

with col5:
    add_vertical_space(3)
    st.subheader(
        resolve_most_practiced_headline(
            dashboard_view, skills=most_practiced_position, skill_type="position"
        )
    )


# Moves Practiced
moves_data = DATA_FETCHER.get_num_times_practiced_skill(
    dashboard_view, skill_type="move"
)
most_practiced_move = DATA_FETCHER.determine_most_practiced_skill(
    moves_data, skill_type="move"
)

with col6:
    st.header("Moves Practiced")
    add_vertical_space(1)
    st.altair_chart(
        altair_chart=create_times_practiced_skill_bar_chart(
            moves_data, skill_type="move"
        ),
        use_container_width=True,
    )

with col7:
    add_vertical_space(3)
    st.subheader(
        resolve_most_practiced_headline(
            dashboard_view, skills=most_practiced_move, skill_type="move"
        )
    )

# Line chart showing number of classes per month
st.header("Number of Classes by Month")

line_chart_data = DATA_FETCHER.get_num_classes_per_month(dashboard_view)

st.altair_chart(
    altair_chart=create_num_classes_by_month_line_chart(
        line_chart_data, dashboard_view=dashboard_view
    ),
    use_container_width=True,
)
