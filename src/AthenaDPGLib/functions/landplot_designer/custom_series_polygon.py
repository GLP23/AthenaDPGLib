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
def painter(sender:int|str, app_data:tuple[dict,list,list,Any,Any,Any]):
    """
    A dpg.custom_series painter function to create the proper polygon shape inside the plot.
    The actual shape of the plot doesn't add any functionality other than any visual benefits.
    """
    # gather all vars we need for the callback
    #   this point is always on 0,0 and 1,1 on the plot
    #   returns the pixel 0,0 and 1,1 would be on
    difference_x = app_data[1][1] - app_data[1][0]
    difference_y = app_data[2][1] - app_data[2][0]

    # Delete old polygon's already drawn shapes
    #   And create new shape
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)

    # draw the main shape
    #   and append the first point to the end to "complete" the polygon
    for polygon in landplot_designer_memory.polygons.values(): #type: Polygon
        points = []
        for _,point in polygon.points:
            x,y, *_ = point
            x_edit = (x*difference_x)+app_data[1][0]
            y_edit = (y*difference_y)+app_data[2][0]
            if x_edit > 10_000 or y_edit > 10_000:
                continue
            else:
                points.append([x_edit,y_edit])

        if points:
            dpg.draw_polygon(
                parent=sender,
                points=points,
                fill=polygon.color,
                color=polygon.color,
                thickness=0,
            )

    # Always make sure to pop the container stack
    dpg.pop_container_stack()
