"""bjj_journey.data_pipeline - Pull and store data used for the BJJ dashboard.

"""
import argparse
from datetime import timedelta
import logging
import os
import re
import time

import google.auth
import gspread
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import Connection, select

from bjj_journey.data_pipeline.checks import check_ids, validate_table
from bjj_journey.database_utils import (
    BJJ_SCHEMA_NAME,
    CLASS_ATTD_TABLE,
    MOVES_PRACTICED_TABLE,
    POSITION_TABLE,
    POSITIONS_PRACTICED_TABLE,
    create_database_engine,
    delete_data_from_table,
    get_metadata,
    query_database,
    reset_sequence,
    update_table,
)

from bjj_journey.utils import load_dotenv_file, set_up_logging


LOGGER = logging.getLogger(__name__)


class BJJDataPipeline:
    """Class which encapsulates logic for pulling and storing BJJ data"""

    BJJ_SPREADSHEET_NAME = "BJJ Dashboard"
    BJJ_WORKSHEET_NAME = "BJJ Total Attendance"
    WORKSHEET_COLS_TO_KEEP = [
        "date",
        "class",
        "class_id",
        "notes",
        "position1",
        "position2",
        "position3",
        "move1",
        "move2",
        "move3",
        "move4",
    ]
    CLASS_ATTENDANCE_TABLE_COLS = ["date", "class_id", "notes"]
    WORKSHEET_COLS_FOR_POSITION_TABLE = [
        "date",
        "class_id",
        "position1",
        "position2",
        "position3",
    ]
    POSITION_TABLE_COLS = ["date", "class_id", "position_id"]
    WORKSHEET_COLS_FOR_MOVE_TABLE = [
        "date",
        "class_id",
        "move1",
        "move2",
        "move3",
        "move4",
    ]
    MOVE_TABLE_COLS = ["date", "class_id", "move_id"]
    # Order matters here - class_attendance should be last
    TABLES_TO_UPDATE = [
        POSITIONS_PRACTICED_TABLE,
        MOVES_PRACTICED_TABLE,
        CLASS_ATTD_TABLE,
    ]
    SEQUENCES_TO_RESET = ["positions_practiced_id_seq", "moves_practiced_id_seq"]

    def __init__(self, user_type: str):
        self.__validate_user_type(user_type)
        self._gspread_client = self.__get_gspread_client(user_type)
        self._db_engine = create_database_engine()
        self._metadata = get_metadata(self._db_engine)

    @staticmethod
    def __validate_user_type(user_type: str) -> None:
        """Validate that the user type is human or machine."""
        allowed_user_types = {"human", "machine"}
        if user_type not in allowed_user_types:
            raise ValueError(
                "The user type must be one of the following values:"
                f" {allowed_user_types}. Got {user_type} instead."
            )

    @staticmethod
    def __get_gspread_client(user_type: str) -> gspread.Client:
        """Authorize gspread based on the user type and return the client.

        Gspread will be authorized via oauth when it is run by a human (i.e. locally
        in dev). Otherwise, it will get credentials via google.auth since this pipeline
        will be running on a Google Cloud Run job in production.
        """
        if user_type == "human":
            return gspread.oauth()

        credentials = google.auth.default(scopes=gspread.auth.DEFAULT_SCOPES)[0]
        return gspread.authorize(credentials)

    def load_data_from_spreadsheet(
        self, spreadsheet_name: str, worksheet_name: str
    ) -> pd.DataFrame:
        """
        Load data from a worksheet within a Google spreadsheet as a pandas DataFrame,
        based on the name of the spreadsheet and worksheet.

        Args:
            spreadsheet_name: the name of the spreadsheet to load data from.
            worksheet_name: the name of the worksheet (within the spreadsheet)
                to load data from.

        Returns:
            a dataframe containing the data from the specified worksheet in the
                specified spreadsheet.
        """
        LOGGER.info("Opening the following Google Spreadsheet: %s", spreadsheet_name)
        spreadsheet = self._gspread_client.open(spreadsheet_name)

        worksheet = spreadsheet.worksheet(worksheet_name)
        data = pd.DataFrame(worksheet.get_all_records())
        LOGGER.info("Loaded data from the following worksheet: %s", worksheet_name)

        return data

    def _get_table_ids(self, table: str) -> pd.DataFrame:
        """Get the ID and name columns from a given table

        Args:
            table: the name of the table to get data for. Allowed values include
                class, position, and move.

        Returns:
            a pandas DataFrame containing the id and name column of the given table

        """
        validate_table(table)

        schema_and_table = f"{BJJ_SCHEMA_NAME}.{table}"

        table_obj = self._metadata.tables[schema_and_table]
        stmt = select(table_obj.c.id, table_obj.c.name)

        LOGGER.info("Getting IDs from %s", schema_and_table)
        table_ids_df = query_database(stmt, con=self._db_engine)

        assert isinstance(table_ids_df, pd.DataFrame)  # make mypy happy
        return table_ids_df

    def _merge_in_table_ids(self, data: pd.DataFrame, table: str) -> pd.DataFrame:
        """Merge IDs into a given dataframe.

        Args:
            data: a pandas DataFrame containing BJJ data. The data should have a column
                with the same name as the given table. This column will be used for the
                merge.
            table: the table whose IDs will get merged into the given dataframe.

        Returns:
            a pandas DataFrame with IDs from the given table merged in
        """
        validate_table(table)

        table_ids = self._get_table_ids(table)
        table_ids = table_ids.rename(columns={"id": f"{table}_id"})
        data = data.merge(table_ids, left_on=table, right_on="name", how="left")

        check_ids(data, name_col=table, id_col=f"{table}_id")

        LOGGER.info("Merged in IDs from %s", f"{BJJ_SCHEMA_NAME}.{table}")

        return data

    def _normalize_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Normalize data pulled from the BJJ spreadsheet.

        Normalization includes:
            - adjusting the column names
            - changing empty strings to NA values
            - adding in class IDs
            - keeping necessary columns only

        Args:
            data: a pandas DataFrame containing data loaded from a worksheet
                within a Google spreadsheet.

        Returns:
            a pandas DataFrame that has been cleaned up in a way that is generally
                applicable for all future bjj database table inserts.
        """

        # Adjust column names
        def adjust_col_names(col):
            """
            Lowercase and remove non-alphanumeric characters from
            given column name
            """
            return re.sub(r"\W+", "", col.lower())

        data = data.rename(mapper=adjust_col_names, axis="columns")

        # Change empty strings to None
        data = data.replace("", None)

        # Add in class IDs
        data = self._merge_in_table_ids(data, table="class")

        # Keep necessary columns
        data = data[self.WORKSHEET_COLS_TO_KEEP]

        return data

    def _prep_data_for_positions_practiced_table(
        self, data: pd.DataFrame
    ) -> pd.DataFrame:
        """Prep data for insertion into bjj.positions_practiced"""
        # Reshape worksheet data from long to wide (each position gets its own row)
        data = data[self.WORKSHEET_COLS_FOR_POSITION_TABLE]
        data = pd.melt(
            data,
            id_vars=["date", "class_id"],
            value_vars=["position1", "position2", "position3"],
            value_name="position",
        )
        data = data.drop(columns=["variable"])

        # Remove records missing a position
        data = data[~data["position"].isna()]

        # Add in position IDs
        data = self._merge_in_table_ids(data, table=POSITION_TABLE)

        # Keep necessary columns
        data = data[self.POSITION_TABLE_COLS]

        return data

    def _prep_data_for_moves_practiced_table(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prep data for insertion into bjj.moves_practiced"""
        # Reshape worksheet data from long to wide (each move gets its own row)
        data = data[self.WORKSHEET_COLS_FOR_MOVE_TABLE]
        data = pd.melt(
            data,
            id_vars=["date", "class_id"],
            value_vars=["move1", "move2", "move3", "move4"],
            value_name="move",
        )
        data = data.drop(columns=["variable"])

        # Remove records missing a move
        data = data[~data["move"].isna()]

        # Add in move IDs
        data = self._merge_in_table_ids(data, table="move")

        # Keep necessary columns
        data = data[self.MOVE_TABLE_COLS]

        return data

    def _update_class_attendance_table(
        self, data: pd.DataFrame, conn: Connection
    ) -> None:
        """Update the bjj.class_attendance table.

        Update methods have a conn parameter so that they can be run as part of a
        transaction.
        """
        data = data[self.CLASS_ATTENDANCE_TABLE_COLS]
        update_table(data, table=CLASS_ATTD_TABLE, con=conn)

    def _update_positions_practiced_table(
        self, data: pd.DataFrame, conn: Connection
    ) -> None:
        """Update the bjj.positions_practiced table.

        Update methods have a conn parameter so that they can be run as part of a
        transaction.
        """
        data = self._prep_data_for_positions_practiced_table(data)
        update_table(data, table=POSITIONS_PRACTICED_TABLE, con=conn)

    def _update_moves_practiced_table(
        self, data: pd.DataFrame, conn: Connection
    ) -> None:
        """Update the bjj.moves_practiced table.

        Update methods have a conn parameter so that they can be run as part of a
        transaction.
        """
        data = self._prep_data_for_moves_practiced_table(data)
        update_table(data, table=MOVES_PRACTICED_TABLE, con=conn)

    def _update_bjj_tables(self, data: pd.DataFrame) -> None:
        """
        Update bjj tables by deleting data from these tables and then inserting
        fresh data pulled from the BJJ spreadsheet.
        """
        with self._db_engine.begin() as conn:
            # Because of foreign key constraints, delete data from positions_practiced
            # and moves_practiced before deleting data from class_attendance.
            for table in self.TABLES_TO_UPDATE:
                delete_data_from_table(table, metadata=self._metadata, con=conn)

            # After deleting, we want to reset sequence
            for sequence in self.SEQUENCES_TO_RESET:
                reset_sequence(sequence, con=conn)

            self._update_class_attendance_table(data, conn=conn)
            self._update_moves_practiced_table(data, conn=conn)
            self._update_positions_practiced_table(data, conn=conn)

    def run(self) -> None:
        """Run the BJJ data pipeline"""
        # Mark the start of the run for measuring execution duration
        LOGGER.info("Begin BJJ data pipeline")
        start_time = time.perf_counter()

        # Pull data from google spreadsheet
        bjj_data = self.load_data_from_spreadsheet(
            self.BJJ_SPREADSHEET_NAME, self.BJJ_WORKSHEET_NAME
        )

        # Get data ready for insert in a general way
        bjj_data = self._normalize_data(bjj_data)

        # Update tables
        self._update_bjj_tables(bjj_data)

        # Measure execution duration
        LOGGER.info("BJJ data pipeline has finished running")
        end_time = time.perf_counter()
        duration = end_time - start_time
        LOGGER.info("Elapsed time: %s", timedelta(seconds=duration))


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        description="Pull and store data for BJJ dashboard"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help=(
            "Increase level of feedback output. Use -vv for even more detail. "
            "Log level defaults to 'WARNING'"
        ),
        action="count",
        default=0,
        dest="verbosity",
    )

    return parser.parse_args()


def main() -> None:
    """Pull BJJ data from Google spreadsheet and store in database tables."""
    args = parse_args()
    set_up_logging(args.verbosity)

    load_dotenv_file()

    # Initialize pipeline
    bjj_pipeline = BJJDataPipeline(os.environ.get("USER_TYPE", "human"))

    # Run pipeline
    bjj_pipeline.run()
