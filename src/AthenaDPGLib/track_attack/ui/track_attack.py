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
from AthenaDPGLib.general.ui.custom_dpg_component import CustomDPGComponent
from AthenaDPGLib.track_attack.models.core import Core
from AthenaDPGLib.general.data.universal_tags import UniversalTags

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
                callback=self.btn_gather_all_projects
            )
            dpg.add_input_text(
                tag="TEST"
            )
            dpg.add_button(
                label="SAVE PROJECT",
                callback=self.btn_save_project
            )
            dpg.add_text(
                tag="TEST_output"
            )
            dpg.add_image(UniversalTags.TA_img_title)

            yield window

    @Core.threaded_executor.threaded_method
    def btn_gather_all_projects(self):
        print(Core.data_tracker.get_all_projects())

    @Core.threaded_executor.threaded_method
    def btn_save_project(self):
        dpg.set_value(
            "TEST_output",
            Core.data_tracker.new_project(name=dpg.get_value("TEST"))
        )

