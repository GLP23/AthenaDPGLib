# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import os
import time
from dataclasses import dataclass, field
import pathlib
import sqlite3

# Custom Library
from AthenaLib.constants.types import PATHLIKE
from AthenaLib.database_connectors.sqlite import ConnectorSqlite3

# Custom Packages
from AthenaDPGLib.track_attack.models.data_interaction.sql_queries import SQLQueries

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class DataInteraction:
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
        self.connector.create_db(queries=SQLQueries.create_db)

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
            cursor.execute(SQLQueries.query_get_all_projects)
            return cursor.fetchall()

    def new_project(self, name:str, info:str=None) -> int:
        """
        Creates a new record on the Database which corresponds to the necessary project information
        Returns the id of the inserted record on the 'Project' table.
        """
        with self.connector.get_cursor(commit=True) as cursor: #type: sqlite3.Cursor
            cursor.execute(SQLQueries.insert_new_project(name, info))
            return cursor.lastrowid

    def change_project(self, project_id:int, name:str=None, info:str=None):
        with self.connector.get_cursor(commit=True) as cursor: #type: sqlite3.Cursor
            cursor.execute(SQLQueries.update_project(project_id, name, info))
            print(cursor.fetchall())
            return cursor.lastrowid


