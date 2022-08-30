# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass
from contextlib import contextmanager

# Custom Library

# Custom Packages
from AthenaDPGLib.models.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.models.landplot_designer.components._component import LandplotDesigner_Component

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Window(CustomDPGItem, LandplotDesigner_Component):
    tag:str

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG Constructor -
    # ------------------------------------------------------------------------------------------------------------------
    @contextmanager
    def constructor(self):
        with dpg.window(tag=self.tag) as window:
            yield window