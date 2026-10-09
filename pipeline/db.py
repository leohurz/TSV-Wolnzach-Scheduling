"""
Thin MySQL access layer shared by every pipeline script.

Previously each script opened its own ad-hoc ``mysql.connector.connect(...)`` call and
duplicated the same cursor/commit/close boilerplate. This module centralises that into a
single context manager plus two small helpers, so connection handling, error logging and
cleanup only need to be written (and fixed) once.

Table names used here always come from the fixed, trusted `TEAM_TABLES` list in
`pipeline.teams` - never from user input - so building SQL with an f-string for the table
name is safe (MySQL does not support parameterised table/column identifiers).
"""
from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any, Iterator, Sequence

import mysql.connector
import pandas as pd

from pipeline.settings import SETTINGS

logger = logging.getLogger(__name__)

# Column order used for every "team schedule" table (h1, d1, u18, ...). Keeping this in one
# place means the scraper (writer) and the Excel builders (readers) can never drift apart.
GAME_COLUMNS = ("spnr", "spt", "team", "liga", "datum", "uhrzeit", "heim", "gast", "halle", "id")


@contextmanager
def get_connection() -> Iterator[Any]:
    """Opens a MySQL connection and guarantees it is closed again, even on error."""
    connection = mysql.connector.connect(
        host=SETTINGS.db_host,
        user=SETTINGS.db_user,
        password=SETTINGS.db_password,
        database=SETTINGS.db_name,
    )
    try:
        yield connection
    finally:
        connection.close()


def fetch_games_df(table_names: Sequence[str]) -> pd.DataFrame:
    """Fetches every row from each of the given team tables into one DataFrame.

    Column names are read from the live schema (``cursor.column_names``) rather than
    assumed, since the real tables may carry extra generated columns (e.g. short-name
    helper columns) beyond the ones the scraper writes via `GAME_COLUMNS`.
    """
    frames: list[pd.DataFrame] = []
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            for table in table_names:
                cursor.execute(f"SELECT * FROM `{table}`")
                frames.append(pd.DataFrame(cursor.fetchall(), columns=cursor.column_names))
        finally:
            cursor.close()
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=GAME_COLUMNS)


def replace_team_games(table_name: str, games: Sequence[tuple]) -> None:
    """Atomically replaces all rows of a single team table with freshly scraped games.

    Uses one ``executemany`` insert instead of looping row-by-row, which is both faster
    and lets us commit (or roll back) the whole refresh as a single unit of work.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"DELETE FROM `{table_name}`")
            if games:
                placeholders = ", ".join(["%s"] * len(GAME_COLUMNS))
                query = (
                    f"INSERT INTO `{table_name}` ({', '.join(GAME_COLUMNS)}) "
                    f"VALUES ({placeholders})"
                )
                cursor.executemany(query, games)
            connection.commit()
        except Exception:
            connection.rollback()
            logger.exception("Failed to refresh table '%s', rolled back", table_name)
            raise
        finally:
            cursor.close()
