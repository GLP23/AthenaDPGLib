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

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def painter(sender:int|str, app_data:tuple[dict,list,list,Any,Any,Any], user_data:tuple[Polygon]):
    """
    A dpg.custom_series painter function to create the proper polygon shape inside the plot.
    The actual shape of the plot doesn't add any functionality other than any visual benefits.
    """
    polygon, = user_data #type: Polygon

    # fixes an issue that relates to quickly redrawing the series
    if not dpg.does_item_exist(sender):
        return

    # gather all vars we need for the callback
    transformed_x = app_data[1]
    transformed_y = app_data[2]

    # Delete old polygon's already drawn shapes
    #   And create new shape
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)

    # draw the main shape
    #   and append the first point to the end to "complete" the polygon
    if points := [list(point) for point in zip(transformed_x, transformed_y)]:
        points.append(points[0])

    dpg.draw_polygon(
        points=points,
        fill=polygon.color_fill,
        color=polygon.color_border,
        thickness=1
    )

    # draw the points afterwards
    #   If this is done first, these will come behind the polygon, which is a desired placement
    for point in zip(transformed_x, transformed_y):
        dpg.draw_circle(point, radius=5, fill=polygon.color_node)

    # Always make sure to pop the container stack
    dpg.pop_container_stack()
