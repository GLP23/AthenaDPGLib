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

from AthenaDPGLib.project_tracking_tool.models.tracker_datahandler import TrackerDataHandler
from AthenaDPGLib.project_tracking_tool.ui.ui_root import UiRoot

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True)
class ProjectTrackingTool:
    sqlite_filepath:PATHLIKE = "project_tracking.db"

    # non init
    tracker_datahandler: TrackerDataHandler = field(init=False)
    ui: CustomDPGComponent = field(init=False)

    # post init vars
    window_tag:InitVar[str] = UniversalTags.PTT

    def __post_init__(self, window_tag: str):
        self.tracker_datahandler = TrackerDataHandler(sqlite_filepath=self.sqlite_filepath)
        self.ui = UiRoot(
            primary_window_tag=window_tag
        )


