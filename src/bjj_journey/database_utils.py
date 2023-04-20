"""bjj_journey.database_utils - Utilities for interacting with the bjj database.

"""
from datetime import datetime
import logging
import os
import urllib.parse

from typing import Tuple, Union
import pandas as pd

from sqlalchemy import (
    Connection,
    CursorResult,
    Delete,
    Engine,
    MetaData,
    Select,
    TextClause,
    create_engine,
    delete,
    text,
)

LOGGER = logging.getLogger(__name__)

HOST_ENV_VAR = "BJJ_DB_HOST"
USER_ENV_VAR = "BJJ_DB_USER"
PASSWORD_ENV_VAR = "BJJ_DB_PWD"
DATABASE_ENV_VAR = "BJJ_DB_DATABASE"
PORT_ENV_VAR = "BJJ_DB_PORT"

DEFAULT_DATABASE_PORT = 5432
BJJ_SCHEMA_NAME = "bjj"

POSITION_TABLE = "position"
MOVE_TABLE = "move"
CLASS_TABLE = "class"
CLASS_ATTD_TABLE = "class_attendance"
POSITIONS_PRACTICED_TABLE = "positions_practiced"
MOVES_PRACTICED_TABLE = "moves_practiced"
CLASS_ATTD_METRICS_TABLE = "class_attendance_metrics"
POSITION_METRICS_TABLE = "position_metrics"
MOVE_METRICS_TABLE = "move_metrics"


def get_database_host() -> str:
    """Return the hostname for the bjj database."""
    if HOST_ENV_VAR in os.environ:
        host = os.environ[HOST_ENV_VAR]
        LOGGER.debug("Using database host: %r", host)
        return host

    raise ValueError(
        "Cannot find bjj database postgresql hostname in the environment variable:"
        f" {HOST_ENV_VAR}"
    )


def get_database_credentials() -> Tuple[str, str]:
    """Return a tuple of the username and password for the bjj database."""
    user = None
    if USER_ENV_VAR in os.environ:
        user = os.environ[USER_ENV_VAR]

    if not user:
        raise ValueError(
            "Cannot find bjj database postgresql user in the environment variable:"
            f" {USER_ENV_VAR}"
        )
    LOGGER.debug("Using database user: %r", user)

    if PASSWORD_ENV_VAR in os.environ:
        pwd = os.environ[PASSWORD_ENV_VAR]
        return user, pwd

    raise ValueError(
        "Cannot find bjj database postgresql password in the environment variable:"
        f" {PASSWORD_ENV_VAR}"
    )


def get_database_name() -> str:
    """Return the database name for the bjj database."""
    if DATABASE_ENV_VAR in os.environ:
        name = os.environ[DATABASE_ENV_VAR]
        LOGGER.debug("Using database name: %r", name)
        return name

    raise ValueError(
        "Cannot find bjj database postgresql name in the environment variable:"
        f" {DATABASE_ENV_VAR}"
    )


def get_database_port() -> int:
    """Return the port for the bjj database."""
    if PORT_ENV_VAR in os.environ:
        port = int(os.environ[PORT_ENV_VAR])
        LOGGER.debug("Using database port: %r", port)

    else:
        port = DEFAULT_DATABASE_PORT
        LOGGER.info(
            (
                "Cannot find database postgresql port in the environment variable (%s)."
                " Using default: %r"
            ),
            PORT_ENV_VAR,
            DEFAULT_DATABASE_PORT,
        )

    return port


def get_database_url(redacted: bool = False) -> str:
    """Return a database connection string with the password optionally redacted."""
    host = get_database_host()
    port = get_database_port()
    name = get_database_name()
    user, pwd = get_database_credentials()
    if redacted:
        pwd = "<REDACTED>"
    else:
        pwd = urllib.parse.quote(pwd, safe="")
    LOGGER.debug(
        "Using database URL: '%s'",
        f"postgresql://{user}:<REDACTED>@{host}:{port}/{name}",
    )
    return f"postgresql://{user}:{pwd}@{host}:{port}/{name}"


def create_database_engine() -> Engine:
    """
    Return an updated sqlalchemy.Engine object connected to
    the appropriate bjj database.
    """
    engine = create_engine(get_database_url(), pool_pre_ping=True)
    return engine


def get_metadata(engine: Engine, schema: str = BJJ_SCHEMA_NAME) -> MetaData:
    """Return metadata reflected from a given engine"""
    metadata = MetaData(schema=schema)
    metadata.reflect(engine, views=True)
    return metadata


def resolve_sql_execution(
    stmt: Union[Select, Delete, TextClause], con: Union[Connection, Engine]
) -> CursorResult:
    """
    Resolve the execution of a sql statement based on the type of
    connection and return the result.
    """
    if isinstance(con, Connection):
        result = con.execute(stmt)
    else:
        with con.begin() as conn:
            result = conn.execute(stmt)
    return result


def query_database(
    stmt: Select, con: Union[Connection, Engine], scalar: bool = False
) -> Union[int, str, bool, datetime, pd.DataFrame]:
    """Query a database table and return the results as a pandas DataFrame.

    Args:
        stmt: a SQLAlchemy Select construct used to select data from a database.
        con: a SQLAlchemy connection to a database. Can either be a
            SQLAlchemy Engine object or a Connection object.
        scalar: indicates if the return output should be a scalar value or not.

    Returns:
        a pandas DataFrame containing the result of the select statement,
            or a scalar value.
    """
    result = resolve_sql_execution(stmt, con)

    if scalar:
        value = result.scalar()

        assert value  # make mypy happy
        return value

    columns = list(result.keys())  # This line is mostly to make mypy happy
    return pd.DataFrame(data=result.fetchall(), columns=columns)


def delete_data_from_table(
    table: str,
    metadata: MetaData,
    con: Union[Connection, Engine],
    schema: str = BJJ_SCHEMA_NAME,
) -> None:
    """Delete data from a given database table.

    Args:
        table: the database table to update.
        metadata: a SQLAlchemy metadata object used to access the relevant Table object.
        con: a SQLAlchemy connection to a database. Can either be a
            SQLAlchemy Engine object or a Connection object.
        schema: the schema of the database table. Defaults to "bjj".
    """
    schema_and_table = f"{schema}.{table}"
    table_to_delete_from = metadata.tables[schema_and_table]
    stmt = delete(table_to_delete_from)
    result = resolve_sql_execution(stmt, con)
    LOGGER.info("Deleted %s rows from table %s", result.rowcount, schema_and_table)


def reset_sequence(
    sequence: str, con: Union[Connection, Engine], schema: str = BJJ_SCHEMA_NAME
) -> None:
    """Reset a given sequence to 0

    Used after deleting all data from a table with a sequence

    Args:
        sequence: the name of the sequence to reset
        con: a SQLAlchemy connection to a database. Can either be a
            SQLAlchemy Engine object or a Connection object.
        schema: the schema of the database table. Defaults to "bjj".
    """
    stmt = text(f"ALTER SEQUENCE {schema}.{sequence} RESTART WITH 1")
    resolve_sql_execution(stmt, con)
    LOGGER.info("Reset the sequence: %s", sequence)


def update_table(
    data: pd.DataFrame,
    table: str,
    con: Union[Connection, Engine],
    schema: str = BJJ_SCHEMA_NAME,
) -> None:
    """
    Update a given database table by inserting the passed-in data.

    Args:
        data: a pandas DataFrame containing the data to update the database table with.
        table: the database table to update.
        con: a SQLAlchemy connection to a database. Can either be a
            SQLAlchemy Engine object or a Connection object.
        schema: the schema of the database table. Defaults to "bjj".
    """
    schema_and_table = f"{schema}.{table}"
    data.to_sql(
        table,
        con=con,
        schema=schema,
        index=False,
        if_exists="append",
        method="multi",
    )
    LOGGER.info("Inserted %s rows into %s", data.shape[0], schema_and_table)
