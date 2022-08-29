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
from AthenaDPGLib.models.landplot_designer.polygon import Polygon
from AthenaDPGLib.models.landplot_designer.components._component import LandplotDesigner_Component

import AthenaDPGLib.functions.landplot_designer.custom_series_polygon as custom_series_polygon

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class LandplotDesigner_Plot(CustomDPGItem, LandplotDesigner_Component):
    tag:str

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG Constructor -
    # ------------------------------------------------------------------------------------------------------------------
    @contextmanager
    def constructor(self):
        with dpg.plot(tag=self.tag, no_menus=True) as plot:
            dpg.add_plot_axis(axis=dpg.mvXAxis,tag=f"{self.tag}_x")
            dpg.add_plot_axis(axis=dpg.mvYAxis,tag=f"{self.tag}_y")

            polygon = Polygon(
                name="test",
                colors=[127, 0, 127]
            )
            self.memory.polygon_selected_name = polygon.name
            self.memory.polygons[polygon.name] = polygon

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
                color=polygon.color_node,
                user_data=polygon,
                callback=self.drag_point_callback
            )
        )
        self.polygon_series_update(polygon=polygon)

    def drag_point_callback(self, sender, app_data, user_data:Polygon):
        polygon:Polygon = user_data
        self.polygon_series_update(polygon=polygon)

    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Series -
    # ------------------------------------------------------------------------------------------------------------------
    def polygon_series_add(self, *,  polygon:Polygon, x:list[float|int]=None, y:list[float|int]=None):
        polygon.series = dpg.add_custom_series(
            x=x if x is not None else [],
            y=y if y is not None else [],
            channel_count=2,
            parent=f"{self.tag}_x",
            callback=custom_series_polygon.painter,
            user_data=(polygon,),
            tag=f"{polygon.name}_series"
        )

    def polygon_series_update(self, polygon:Polygon):
        # check as soon as possible if the polygon is actually creatable
        if (polygon.name not in self.memory.polygons) or (len((points := polygon.points)) <= 2):
            return

        # assemble all the points
        #   todo offload this unpacking to the stored values in the column
        x_data = [dpg.get_value(p)[0] for p in points]
        y_data = [dpg.get_value(p)[1] for p in points]

        # create a new polygon if it doesn't exist yet
        if not dpg.does_item_exist(f"{polygon.name}_series"):
            self.polygon_series_add(polygon=polygon, x=x_data, y=y_data)

        elif len(x_data) == len(dpg.get_value(f"{polygon.name}_series")[0]):
            dpg.set_value(f"{polygon.name}_series", [x_data, y_data])

        else:
            # this assumes that the node count in the polygon has changed
            #   And allows us to delete the old one and create a new polygon
            dpg.delete_item(f"{polygon.name}_series")
            self.polygon_series_add(polygon=polygon, x=x_data, y=y_data)
