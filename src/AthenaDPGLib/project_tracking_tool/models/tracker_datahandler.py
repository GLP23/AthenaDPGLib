# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import pathlib

# Custom Library
from AthenaLib.constants.types import PATHLIKE
from AthenaLib.database_connectors.sqlite import ConnectorSqlite3

# Custom Packages
from AthenaDPGLib.general.functions.threaded_executor import get_threaded_executor
from AthenaDPGLib.project_tracking_tool.data.sqlite_tracker import SQLITE_CREATE_FILE_QUERIES

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class TrackerDataHandler:
    sqlite_filepath:PATHLIKE

    # non init
    connector:ConnectorSqlite3 = field(init=False)

    def __post_init__(self):
        self.connector = ConnectorSqlite3(path=self.sqlite_filepath)

        if not pathlib.Path(self.sqlite_filepath).exists():
            self.connector.create_file(
                queries=SQLITE_CREATE_FILE_QUERIES
            )
