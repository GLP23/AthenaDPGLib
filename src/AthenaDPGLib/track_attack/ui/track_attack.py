# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from contextlib import contextmanager
from dataclasses import dataclass

# Custom Library

# Custom Packages
from AthenaDPGLib.general.functions.threaded_executor import threaded_method
from AthenaDPGLib.general.ui.custom_dpg_component import CustomDPGComponent
from AthenaDPGLib.track_attack.models.core import Core

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True)
class TrackAttack(CustomDPGComponent):
    """
    Credits:
        Name of 'Track Attack' by Wh4i3
    """
    primary_window_tag:str

    @contextmanager
    def dpg(self):
        with dpg.window(tag=self.primary_window_tag) as window:
            dpg.add_text("hello worlds")
            dpg.add_button(
                label="Gather_all_projects",
            )

            yield window


