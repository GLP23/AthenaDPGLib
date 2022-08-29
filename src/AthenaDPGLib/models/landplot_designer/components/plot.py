# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field
from contextlib import contextmanager

# Custom Library

# Custom Packages
from AthenaDPGLib.models.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.models.landplot_designer.polygon import Polygon
from AthenaDPGLib.models.landplot_designer.components._component import LandplotDesigner_Component

import AthenaDPGLib.functions.landplot_designer.custom_series_polygon as custom_series_polygon

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Plot(CustomDPGItem, LandplotDesigner_Component):
    tag:str

    #non init
    axis_x: str = field(init=False)
    axis_y: str = field(init=False)

    def __post_init__(self):
        self.axis_x = f"{self.tag}_x"
        self.axis_y = f"{self.tag}_y"

        self.memory.plot_tag =  self.tag
        self.memory.plot_axis_y_tag = self.axis_y

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG Constructor -
    # ------------------------------------------------------------------------------------------------------------------
    @contextmanager
    def constructor(self):
        with dpg.plot(tag=self.tag, no_menus=True, width=750, height=750) as plot:
            dpg.add_plot_axis(axis=dpg.mvXAxis,tag=self.axis_x)
            dpg.add_plot_axis(axis=dpg.mvYAxis,tag=self.axis_y)

            yield plot

        # after everything is constructed, assign the registries
        self.item_handler_registries()

    # ------------------------------------------------------------------------------------------------------------------
    # - item handler registries -
    # ------------------------------------------------------------------------------------------------------------------
    def item_handler_registries(self):
        with dpg.item_handler_registry(tag=f"{self.tag}_registry"):
            dpg.add_item_clicked_handler(
                button=dpg.mvMouseButton_Left,
                callback=self.mousebutton_left
            )

        dpg.bind_item_handler_registry(item=self.tag,handler_registry=f"{self.tag}_registry")

    def mousebutton_left(self):
        if self.memory.polygon_selected:
            self.add_drag_point(
                polygon=self.memory.polygon_selected
            )

    def add_drag_point(self,polygon:Polygon):
        # assign the drag point to the list of points to the polygon
        polygon.points.append(
            dpg.add_drag_point(
                parent=self.tag,
                default_value=dpg.get_plot_mouse_pos(),
                label=polygon.name,
                color=[255,255,255,255],
                user_data=polygon,
                callback=self.drag_point_callback
            )
        )

        # if a series already exists, delete it and clean it up
        if polygon.series is not None:
            dpg.delete_item(polygon.series)

        # Create a new series with the updated points
        custom_series_polygon.new(
            polygon=polygon,
            x=[dpg.get_value(p)[0] for p in polygon.points],
            y=[dpg.get_value(p)[1] for p in polygon.points]
        )

    def drag_point_callback(self, _, __, polygon:Polygon):
        """
        Function called to update the series with new points on the given polygon
        """
        dpg.set_value(
            item=polygon.series,
            value=[[dpg.get_value(p)[0] for p in polygon.points],[dpg.get_value(p)[1] for p in polygon.points]]
        )
