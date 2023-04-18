"""bjj_journey.streamlit_app.data - Retrieve data for the BJJ dashboard app.

"""
from datetime import datetime
from typing import List
import pandas as pd
from sqlalchemy import func, select

from bjj_journey.database_utils import (
    BJJ_SCHEMA_NAME,
    CLASS_ATTD_METRICS_TABLE,
    CLASS_ATTD_TABLE,
    MOVE_METRICS_TABLE,
    POSITION_METRICS_TABLE,
    create_database_engine,
    get_metadata,
    query_database,
)
from bjj_journey.streamlit_app.utils import validate_skill_type


class BJJDataFetcher:
    """Fetch data for BJJ dashboard"""

    NUM_MONTHS_TRAINED_METRIC = "num_months_trained"
    NUM_CLASSES_ATTENDED_METRIC = "num_classes_attended"
    NUM_CLASS_MIN_METRIC = "num_class_minutes"
    NUM_TIMES_PRACTICED_METRIC = "num_times_practiced"

    def __init__(self):
        self._db_engine = create_database_engine()
        self._metadata = get_metadata(self._db_engine)

    @staticmethod
    def _resolve_agg_category(dashboard_view: str) -> str:
        """Get the aggregation category based on the dashboard view"""
        try:
            int(dashboard_view)
            return "year"
        except ValueError:
            return "overall"

    def _get_metric_value(
        self, table: str, metric_name: str, agg_category: str, agg_value: str
    ) -> int:
        """Get the metric value based on the inputs"""
        metric_table = self._metadata.tables[f"{BJJ_SCHEMA_NAME}.{table}"]
        agg_category = self._resolve_agg_category(agg_category)
        stmt = (
            select(metric_table.c.metric_value)
            .where(metric_table.c.metric_name == metric_name)
            .where(metric_table.c.aggregation_category == agg_category)
            .where(metric_table.c.aggregation_value == agg_value)
        )
        metric_value = query_database(stmt, con=self._db_engine, scalar=True)

        assert isinstance(metric_value, int)  # make mypy happy
        return metric_value

    def get_most_recent_update_date(self) -> str:
        """Get the most recent date the data was updated."""
        class_attd_table = self._metadata.tables[
            f"{BJJ_SCHEMA_NAME}.{CLASS_ATTD_TABLE}"
        ]
        # Pylint is flagging func.max not callable because it can't analyze the
        # func object statically and determine that it has a max method.
        stmt = select(
            func.max(class_attd_table.c.updated_at)  # pylint: disable=not-callable
        )
        date = query_database(stmt, con=self._db_engine, scalar=True)

        assert isinstance(date, datetime)  # make mypy happy
        return date.strftime("%Y-%m-%d")

    def get_time_spent_training(self, dashboard_view: str) -> str:
        """Get total time spent training based on the dashboard view."""
        months_trained = self._get_metric_value(
            table=CLASS_ATTD_METRICS_TABLE,
            metric_name=self.NUM_MONTHS_TRAINED_METRIC,
            agg_category=dashboard_view,
            agg_value=dashboard_view.lower(),
        )
        return f"{months_trained} months"

    def get_number_of_classes_attended(self, dashboard_view: str) -> int:
        """Get the total number of classes attended based on the dashboard view."""
        return self._get_metric_value(
            table=CLASS_ATTD_METRICS_TABLE,
            metric_name=self.NUM_CLASSES_ATTENDED_METRIC,
            agg_category=dashboard_view,
            agg_value=dashboard_view.lower(),
        )

    def get_total_class_hours(self, dashboard_view: str) -> float:
        """Get total class hours based on the dashboard view."""
        total_class_min = self._get_metric_value(
            table=CLASS_ATTD_METRICS_TABLE,
            metric_name=self.NUM_CLASS_MIN_METRIC,
            agg_category=dashboard_view,
            agg_value=dashboard_view.lower(),
        )
        return total_class_min / 60

    def get_num_times_practiced_skill(
        self, dashboard_view: str, skill_type: str
    ) -> pd.DataFrame:
        """
        Get the number of times a skill was practiced based on the dashboard view
        and the skill type.

        Valid skill types include "move" and "position".
        """
        validate_skill_type(skill_type)

        if skill_type == "position":
            table = self._metadata.tables[f"{BJJ_SCHEMA_NAME}.{POSITION_METRICS_TABLE}"]
            stmt = select(
                table.c.position, table.c.aggregation_value, table.c.metric_value
            )
        else:
            table = self._metadata.tables[f"{BJJ_SCHEMA_NAME}.{MOVE_METRICS_TABLE}"]
            stmt = select(table.c.move, table.c.aggregation_value, table.c.metric_value)

        agg_category = self._resolve_agg_category(dashboard_view)
        stmt = (
            stmt.where(table.c.metric_name == self.NUM_TIMES_PRACTICED_METRIC)
            .where(table.c.aggregation_category == agg_category)
            .where(table.c.aggregation_value == dashboard_view.lower())
        )

        data = query_database(stmt, con=self._db_engine)
        assert isinstance(data, pd.DataFrame)  # make mypy happy

        data = data.rename(
            columns={
                "metric_value": "num_times_practiced",
            }
        )
        return data

    def determine_most_practiced_skill(
        self, data: pd.DataFrame, skill_type: str
    ) -> List:
        """Determine the most practiced skill based on the given data and skill type.

        Valid skill types include "move" and "position".
        """
        validate_skill_type(skill_type)

        max_practice_num = data["num_times_practiced"].max()
        most_practiced = data[data["num_times_practiced"] == max_practice_num][
            skill_type
        ].values
        return list(most_practiced)

    def get_num_classes_per_month(self, dashboard_view: str) -> pd.DataFrame:
        """Get the number of classes attended per month based on the dashboard view."""
        table = self._metadata.tables[f"{BJJ_SCHEMA_NAME}.{CLASS_ATTD_METRICS_TABLE}"]
        stmt = (
            select(table)
            .where(table.c.metric_name == self.NUM_CLASSES_ATTENDED_METRIC)
            .where(table.c.aggregation_category == "month")
        )

        data = query_database(stmt, con=self._db_engine)
        assert isinstance(data, pd.DataFrame)  # make mypy happy

        data = data.rename(
            columns={"metric_value": "num_classes", "aggregation_value": "month"}
        )

        data["month"] = pd.to_datetime(data["month"])
        data["year"] = data["month"].dt.strftime("%Y")
        data["month"] = data["month"].dt.strftime("%m")

        if dashboard_view != "Overall":
            data = data[data["year"] == dashboard_view]

        return data
