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
        self.memory.plot_axis_x_tag = self.axis_x

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG Constructor -
    # ------------------------------------------------------------------------------------------------------------------
    @contextmanager
    def constructor(self):
        with dpg.plot(tag=self.tag, no_menus=True) as plot:
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
                default_value=(pos:=dpg.get_plot_mouse_pos()),
                label=polygon.name,
                color=polygon.color,
                user_data=(polygon, ),
                callback=self.drag_point_callback
            )
        )
        if polygon.series is None:
            custom_series_polygon.new(polygon=polygon, x=[pos[0]], y=[pos[1]])
        self.polygon_series_update(polygon=polygon)

    def drag_point_callback(self, sender, app_data, user_data:tuple[Polygon]):
        polygon, = user_data
        self.polygon_series_update(polygon=polygon)

    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Series -
    # ------------------------------------------------------------------------------------------------------------------
    def polygon_series_update(self, polygon:Polygon):
        """
        Function called to update the series with new points on the given polygon
        """
        # check as soon as possible if the polygon is actually creatable
        if (polygon.name not in self.memory.polygons) or (len((points := polygon.points)) <= 2):
            return

        # assemble all the points
        #   todo offload this unpacking to the stored values in the column
        x_data = [dpg.get_value(p)[0] for p in points]
        y_data = [dpg.get_value(p)[1] for p in points]

        # create a new polygon if it doesn't exist yet
        if len(x_data) == len(dpg.get_value(polygon.series)[0]):
            dpg.set_value(polygon.series, [x_data, y_data])
            return

        # this assumes that the node count in the polygon has changed
        #   And allows us to delete the old one and create a new polygon
        #   Else the custom series will make DPG crash
        dpg.delete_item(polygon.series)
        custom_series_polygon.new(polygon=polygon, x=x_data, y=y_data)
