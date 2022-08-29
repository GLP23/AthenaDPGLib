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
        with dpg.plot(tag=self.tag, no_menus=True, width=750, height=750, no_title=True) as plot:
            dpg.add_plot_axis(axis=dpg.mvXAxis,tag=self.axis_x, no_tick_marks=True, no_tick_labels=True)
            with dpg.plot_axis(axis=dpg.mvYAxis,tag=self.axis_y, no_tick_marks=True, no_tick_labels=True):
                # one global series which controls the polygon painting
                #   No real polygon is stored withing it,
                #       as the drag points are parented to the plot and nit the series
                dpg.add_custom_series(
                    x=[0,1],
                    y=[0,1],
                    channel_count=2,
                    callback=custom_series_polygon.painter,
                )

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
        pos = dpg.get_plot_mouse_pos()
        polygon.points.append(
            [
                dpg.add_drag_point(
                    parent=self.tag,
                    default_value=pos,
                    label=polygon.name,
                    color=[255,255,255,255],
                    callback=self.drag_point_callbck,
                    user_data=polygon
                ),
                pos
            ]
        )

    def drag_point_callbck(self, sender, __, polygon:Polygon):
        for i, (point, _) in enumerate(polygon.points):
            if point == sender:
                polygon.points[i][1] = dpg.get_value(sender)