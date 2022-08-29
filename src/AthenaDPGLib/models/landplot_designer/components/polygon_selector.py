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

import AthenaDPGLib.functions.landplot_designer.custom_series_polygon as custom_series_polygon

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class PolygonSelector(CustomDPGItem, LandplotDesigner_Component):
    tag:str

    inputtxt_polygon_name:str = "inputtxt_polygon_name"
    tbl_polygons:str = "tbl_polygons"

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
            with dpg.table(tag=self.tbl_polygons, policy=dpg.mvTable_SizingStretchProp):
                dpg.add_table_column(label="", width=50)
                dpg.add_table_column(label="Name")
                dpg.add_table_column(label="Editors")

            yield group

    # ------------------------------------------------------------------------------------------------------------------
    # - New Polygon callbacks -
    # ------------------------------------------------------------------------------------------------------------------
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
        self.table_row_add(polygon)

    def table_row_add(self, polygon:Polygon):
        with dpg.table_row(parent=self.tbl_polygons):
            # column 1
            dpg.add_checkbox(
                user_data=polygon.name,
                callback=self.checkbox_callback,
            )
            # column 2
            dpg.add_text(default_value=polygon.name)

            # column 3
            with dpg.group(horizontal=True):
                dpg.add_color_edit(
                    tag=f"{polygon.name}_color_edit",
                    default_value=polygon.color,
                    callback=lambda _,__,user_data: setattr(
                        user_data,
                        "color",
                        dpg.get_value(f"{user_data.name}_color_edit")
                    ),
                    user_data = polygon,
                    no_inputs=True,
                )

    def checkbox_callback(self, sender, app_data, user_data):
        if app_data:
            self.memory.polygon_selected_name = user_data

        else:
            self.memory.polygon_selected_name = NOTHING