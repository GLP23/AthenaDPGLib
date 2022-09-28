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
from AthenaDPGLib.general.data.universal_tags import UniversalTags
from AthenaDPGLib.general.ui.custom_dpg_component import CustomDPGComponent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True)
class UiRoot(CustomDPGComponent):
    primary_window_tag:str

    @contextmanager
    def dpg(self):
        with dpg.window(tag=self.primary_window_tag) as window:
            dpg.add_text("hello worlds")
            dpg.add_button(
                label="press me",
            )

            yield window
