# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import Any

# Custom Library

# Custom Packages
from AthenaDPGLib.models.landplot_designer.polygon import Polygon
from AthenaDPGLib.data.landplot import landplot_designer_memory

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def new(*,  polygon:Polygon, x:list[float|int], y:list[float|int]):
    """
    Adds a polygon to the plot.
    """
    # define the tag to be used for the series
    #   this way it can be used anywhere throughout the landplot designer
    #   as the polygon is stored in the memory class
    polygon.series = dpg.add_custom_series(
        x=x,
        y=y,
        channel_count=2,
        parent=landplot_designer_memory.plot_axis_y_tag,
        user_data=polygon,
        callback=painter,
    )


def painter(sender:int|str, app_data:tuple[dict,list,list,Any,Any,Any], polygon:Polygon):
    """
    A dpg.custom_series painter function to create the proper polygon shape inside the plot.
    The actual shape of the plot doesn't add any functionality other than any visual benefits.
    """
    # fixes an issue that relates to quickly redrawing the series
    if not dpg.does_item_exist(sender):
        return

    # gather all vars we need for the callback
    transformed_x = app_data[1]
    transformed_y = app_data[2]
    if not transformed_y or not transformed_x:
        return


    # Delete old polygon's already drawn shapes
    #   And create new shape
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)

    # draw the main shape
    #   and append the first point to the end to "complete" the polygon
    dpg.draw_polygon(
        parent=sender,
        points=(points := [[x,y] for x,y in zip(transformed_x, transformed_y)]),
        fill=polygon.color,
        color=polygon.color,
        thickness=0,
    )

    # draw the points afterwards
    #   If this is done first, these will come behind the polygon, which is a desired placement
    if polygon.nodes_enabled:
        for point in points:
            dpg.draw_circle(
                point,
                parent=sender,
                radius=5,
                fill=[255,255,255,255],
                color=[0,0,0,255],
                thickness=5
            )

    # Always make sure to pop the container stack
    dpg.pop_container_stack()
