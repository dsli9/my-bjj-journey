"""bjj_journey.data_pipeline.checks

Data quality checks and validations.
"""
import pandas as pd


def check_ids(data: pd.DataFrame, name_col: str, id_col: str) -> None:
    """Check that all records are associated with an ID"""
    records_missing_id = set(data[data[id_col].isna()][name_col])
    assert (
        not records_missing_id
    ), f"The following records are missing a {name_col} id: {records_missing_id}"


def validate_table(table: str) -> None:
    """
    Validate that the passed-in table is one of the following: class, move, position
    """
    allowed_tables = {"class", "move", "position"}
    if table not in allowed_tables:
        raise ValueError(
            f"The table argument must be one of the following values: {allowed_tables}."
            f" Got {table} instead."
        )
