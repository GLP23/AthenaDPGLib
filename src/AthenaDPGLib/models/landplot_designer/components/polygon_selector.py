# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass
from contextlib import contextmanager
import random
import threading

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
            dpg.add_text("Polygon render test of 10_000 polygons with 4 points each")
            dpg.add_text()
            with dpg.group(horizontal=True):
                dpg.add_button(label="pregenerate", callback=self.pre_gen)
                dpg.add_text("Rendered polygons :")
                dpg.add_text(tag="render_amount")
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
            with dpg.table(tag=self.tbl_polygons, policy=dpg.mvTable_SizingStretchProp, scrollY=True):
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

        dpg.set_value(self.inputtxt_polygon_name, NOTHING)

        self.table_row_add(polygon)
        self.memory.polygon_add(polygon=polygon)

    def table_row_add(self, polygon:Polygon):
        with dpg.table_row(parent=self.tbl_polygons):
            # column 1
            dpg.add_checkbox(
                user_data=polygon,
                callback=self.checkbox_callback,
            )
            # column 2
            dpg.add_text(default_value=polygon.name)

            # column 3
            with dpg.group(horizontal=True):
                dpg.add_color_edit(
                    tag=f"{polygon.name}_color_edit",
                    default_value=polygon.color,
                    callback=self.color_edit_callback,
                    user_data = polygon,
                    no_inputs=True,
                )

    def checkbox_callback(self, sender, app_data:bool, polygon:Polygon):

        polygon.nodes_enabled = app_data

        # with self.memory.polygons_pause_render():
        for point, _ in polygon.points:
            dpg.show_item(point) if app_data else dpg.hide_item(point)

        if app_data:
            self.memory.polygon_selected_name = polygon.name
            for row in dpg.get_item_children(self.tbl_polygons)[1]:
                if (checkbox := dpg.get_item_children(row)[1][0]) == sender:
                    continue

                polygon_checkbox = dpg.get_item_user_data(checkbox)  # type: Polygon
                dpg.set_value(checkbox, False)
                polygon_checkbox.nodes_enabled = False
                for point, _ in polygon_checkbox.points:
                    dpg.hide_item(point)
        else:
            self.memory.polygon_selected_name = NOTHING

    def color_edit_callback(self, sender,_, polygon):
        polygon.color = dpg.get_value(sender)

    # ------------------------------------------------------------------------------------------------------------------
    # - pregen -
    # ------------------------------------------------------------------------------------------------------------------
    def pre_gen(self):
        rectangle = (
            (0,0),
            (0,1),
            (1,1),
            (1,0),
        )
        with self.memory.polygons_pause_render():
            for i in range(1_000):
                polygon: Polygon = Polygon(
                    name=(name := f"{i}"),
                    color=(random.randint(0,255),random.randint(0,255),255,255)
                )
                polygon.points = [
                    [
                        dpg.add_drag_point(
                            parent=self.memory.plot_tag,
                            default_value=(pos := (x + i, y + i)),
                            label=name,
                            callback=self.drag_point_callbck,
                            user_data=polygon
                        ),
                        pos
                    ]
                    for x, y in rectangle
                ]

                self.table_row_add(polygon)
                self.memory.polygons[polygon.name] = polygon

    def drag_point_callbck(self, sender, __, polygon: Polygon):
        for i, (point, _) in enumerate(polygon.points):
            if point == sender:
                polygon.points[i][1] = dpg.get_value(sender)