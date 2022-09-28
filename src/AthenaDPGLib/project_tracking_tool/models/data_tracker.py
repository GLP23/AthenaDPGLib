# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import os
from dataclasses import dataclass, field
import pathlib
import sqlite3

# Custom Library
from AthenaLib.constants.types import PATHLIKE
from AthenaLib.database_connectors.sqlite import ConnectorSqlite3

# Custom Packages
import AthenaDPGLib.project_tracking_tool.functions.data_tracker as SQL

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class DataTracker:
    db:PATHLIKE

    # non init
    _db_path:pathlib.Path = field(init=False)
    connector:ConnectorSqlite3 = field(init=False)

    def __post_init__(self):
        self.connector = ConnectorSqlite3(path=self.db)
        self._db_path = pathlib.Path(self.db)

        if not self._db_path.exists():
            self.db_create()

    # ------------------------------------------------------------------------------------------------------------------
    # - Database operations -
    # ------------------------------------------------------------------------------------------------------------------
    def db_delete(self):
        """
        Removes the DB file
        """
        os.remove(self._db_path)

    def db_create(self):
        """
        Creates the DB file, populates the database with the correct table setup and inserts any prerequisite records
        """
        self.connector.create_db(queries=SQL.CREATE_DB)

    def db_reset(self):
        """
        Resets the DB file, removing it first and creating it from the ground up again
        """
        self.db_delete()
        self.db_create()

    # ------------------------------------------------------------------------------------------------------------------
    # - Project related functions -
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_projects(self) -> list[tuple[int,str,str]]:
        """
        Retrieve a list of all projects as records from the 'Projects' table
        """
        with self.connector.get_cursor() as cursor: #type: sqlite3.Cursor
            cursor.execute(SQL.QUERY_GET_ALL_PROJECTS)
            return cursor.fetchall()

    def new_project(self, name:str, info:str=None) -> int:
        """
        Creates a new record on the Database which corresponds to the necessary project information
        Returns the id of the inserted record on the 'Project' table.
        """
        with self.connector.get_cursor(commit=True) as cursor: #type: sqlite3.Cursor
            cursor.execute(SQL.insert_new_project(name, info))
            return cursor.lastrowid

