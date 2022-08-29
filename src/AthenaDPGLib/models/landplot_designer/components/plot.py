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
            self.memory.selected_polygon = polygon.name
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
        # check if there is at least a selected polygon
        if dpg.is_mouse_button_dragging(button=dpg.mvMouseButton_Left, threshold=0.05):
            return

        self.add_drag_point(
            polygon=(polygon := self.memory.polygons[self.memory.selected_polygon])
        )

    def add_drag_point(self, polygon:Polygon):
        # assign the drag point to the list of points to the polygon
        polygon.points.append(
            dpg.add_drag_point(
                parent=self.tag,
                default_value=dpg.get_plot_mouse_pos(),
                label=polygon.name,
                color=polygon.color_node,
                user_data=polygon.name,
                callback=self.polygon_series_update
            )
        )
        self.polygon_series_update(dpg.last_item(),dpg.last_item(),polygon.name)

    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Series -
    # ------------------------------------------------------------------------------------------------------------------
    def add_polygon_series(self, *,  polygon:Polygon, x:list[float|int]=None, y:list[float|int]=None):
        polygon.series = dpg.add_custom_series(
            x=x if x is not None else [],
            y=y if y is not None else [],
            channel_count=2,
            parent=f"{self.tag}_x",
            callback=self.polygon_series_callback,
            user_data=polygon.name,
            tag=f"{polygon.name}_series"
        )

    def polygon_series_update(self,sender, app_data, user_data):
        polygon:Polygon = self.memory.polygons[user_data]
        all_positions = [(x,y) for x,y,*_ in dpg.get_values(polygon.points)]

        if dpg.does_item_exist(f"{polygon.name}_series"):
            dpg.delete_item(f"{polygon.name}_series")

        self.add_polygon_series(
            polygon=polygon,
            x=[x for x, _ in all_positions],
            y=[y for _, y in all_positions]
        )

    def polygon_series_callback(self,sender, app_data, user_data):
        # fixes an issue that relates to quickly redrawing the series
        if not dpg.does_item_exist(sender):
            return
        
        polygon:Polygon = self.memory.polygons[user_data]

        # gather all vars we need for the callback
        transformed_x = app_data[1]
        transformed_y = app_data[2]

        # Delete old polygon and create new items
        dpg.delete_item(sender, children_only=True, slot=2)
        dpg.push_container_stack(sender)

        # draw the main shape
        #   and append the first point to the end to "complete" the polygon
        dpg.draw_polygon(
            points=[list(point) for point in zip(transformed_x, transformed_y)],
            # color=polygon.color_border,
            fill=polygon.color_fill,
            thickness=0
        )

        # draw the points afterwards
        #   If this is done first, these will come behind the polygon, which is not what we want
        for point in zip(transformed_x, transformed_y):
            dpg.draw_circle(point, radius=50, fill=polygon.color_node)

        # Always make sure to pop the container stack
        dpg.pop_container_stack()
