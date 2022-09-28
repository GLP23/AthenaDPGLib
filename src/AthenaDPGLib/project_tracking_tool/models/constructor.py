# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from contextlib import contextmanager
from dataclasses import dataclass, field, InitVar

# Custom Library
from AthenaLib.constants.types import PATHLIKE

# Custom Packages
from AthenaDPGLib.general.data.universal_tags import UniversalTags
from AthenaDPGLib.general.functions.threaded_executor import get_threaded_executor
from AthenaDPGLib.general.ui.custom_dpg_component import CustomDPGComponent

from AthenaDPGLib.project_tracking_tool.models.data_tracker import DataTracker
from AthenaDPGLib.project_tracking_tool.ui.ui_root import UiRoot

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True)
class Constructor:
    # post init vars
    window_tag: InitVar[str] = UniversalTags.PTT
    sqlite_filepath: InitVar[PATHLIKE] = "project_tracking.db"

    # non init
    data_tracker: DataTracker = field(init=False)
    ui: CustomDPGComponent = field(init=False)

    def __post_init__(self, window_tag: str, sqlite_filepath:PATHLIKE):
        self.data_tracker = DataTracker(db=sqlite_filepath)
        self.ui = UiRoot(
            primary_window_tag=window_tag
        )


