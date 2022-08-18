# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import sqlite3
import pathlib
import contextlib

# Custom Library

# Custom Packages
from AthenaDPGLib.data.sql import SHOW_TABLES, TRANSLATION_CREATE_EMPTY_TABLES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Translator:
    sqlite_filepath:str

    def __init__(self, sqlite_filepath:str):
        # Check if the sqlite file is actually present
        self.sqlite_filepath = sqlite_filepath

        # validate if the file is present and create when not there
        if not pathlib.Path(self.sqlite_filepath).exists():
            # creates the file and creates tables
            self.fix_missing_file()
        else:
            # only validates tables and creates missing tables
            self.validate_structure()

    # ------------------------------------------------------------------------------------------------------------------
    # - Connection and Cursor context managers -
    # ------------------------------------------------------------------------------------------------------------------
    @contextlib.contextmanager
    def connection(self) -> sqlite3.Connection:
        """
        Context Managed function to yield the connection to any function that needs it.
        Closes the connection automatically
        """

        # Context manage the connection
        #   Done so the connection always auto closes
        with contextlib.closing(sqlite3.connect(self.sqlite_filepath)) as conn: #type:  sqlite3.Connection
            yield conn

    @contextlib.contextmanager
    def cursor(self, conn:sqlite3.Connection = None) -> sqlite3.Cursor:
        """
        Context Managed function to yield the cursor to any function that needs it.
        Calls the Translator.gather_connection() first to have the connection managed through there.
        Closes the cursor automatically
        """

        # Context manage the cursor
        #   Done so the connection always auto closes
        if conn is None:
            with self.connection() as conn_:
                with contextlib.closing(conn_.cursor()) as cursor:
                    yield cursor
        else:
            with contextlib.closing(conn.cursor()) as cursor:
                yield cursor

    # ------------------------------------------------------------------------------------------------------------------
    # - Preliminary Check and fixes if tables don't exist -
    # ------------------------------------------------------------------------------------------------------------------
    def validate_structure(self):
        """
        Method that validates the structure of the sqlite file meant for translations.
        Creates new tables if they don't exist yet and crashes if unknown tables exist.

        """
        known_tables = set()

        # gather all tables and make sure the structure is valid
        with self.connection() as conn:
            with self.cursor(conn=conn) as cur:
                tables:list[tuple[str,]] = list(cur.execute(SHOW_TABLES))
                for table , in tables: # need a comma here because if not table is a tuple[str] where str is table name
                    if table not in TRANSLATION_CREATE_EMPTY_TABLES:
                        raise ValueError(f"Unknown table found in the sqlite file: `{table}`")
                    known_tables.add(table)

            # create tables that don't exist in the sqlite file ye
            with self.cursor(conn=conn) as cur:
                for expected_table, sql in TRANSLATION_CREATE_EMPTY_TABLES.items():
                    if expected_table not in known_tables:
                        cur.execute(sql)

        return known_tables

    def fix_missing_file(self):
        with self.cursor() as cursor:
            for _ , sql in TRANSLATION_CREATE_EMPTY_TABLES.items():
                cursor.execute(sql)