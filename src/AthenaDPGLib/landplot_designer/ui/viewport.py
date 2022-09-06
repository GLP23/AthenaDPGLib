# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import contextlib
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.ui.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.landplot_designer.models.core import Core

from AthenaDPGLib.general.data.universal_tags import LandplotItems

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Viewport(CustomDPGItem):
    # ------------------------------------------------------------------------------------------------------------------
    # - DPG methods -
    # ------------------------------------------------------------------------------------------------------------------
    def add_dpg(self, **kwargs):
        with self.dpg(**kwargs):
            pass

    @contextlib.contextmanager
    def dpg(self, **kwargs) -> None:
        # noinspection PyNoneFunctionAssignment
        LandplotItems.viewport = dpg.create_viewport(title="Directive Athena: Landplot Designer")
        yield LandplotItems.viewport
