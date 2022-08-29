# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass
from contextlib import contextmanager

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaDPGLib.models.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.models.landplot_designer.components._component import LandplotDesigner_Component
from AthenaDPGLib.models.landplot_designer.polygon import Polygon

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class PolygonSelector(CustomDPGItem, LandplotDesigner_Component):
    tag:str

    inputtxt_polygon_name:str = "inputtxt_polygon_name"

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG Constructor -
    # ------------------------------------------------------------------------------------------------------------------
    @contextmanager
    def constructor(self):
        with dpg.group(tag=self.tag) as group:
            dpg.add_text("Create a new polygon with a unique name:")
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    tag=self.inputtxt_polygon_name,
                    on_enter=True,
                    width=500,
                    callback=self.polygon_new_callback
                )
                dpg.add_button(
                    label="Save Polygon",
                    callback=self.polygon_new_callback
                )

            yield group

    def polygon_new_callback(self):
        polygon_name = dpg.get_value(self.inputtxt_polygon_name)
        if not polygon_name or polygon_name is None:
            print("NO NAME GIVEN")
            return

        if polygon_name in self.memory.polygons:
            print("NAME WAS ALREADY IN USE")
            return

        # Create the new polygon with the corresponding data
        polygon:Polygon = Polygon(
            name=polygon_name
        )

        self.memory.polygon_add(polygon=polygon)
        dpg.set_value(self.inputtxt_polygon_name, NOTHING)
