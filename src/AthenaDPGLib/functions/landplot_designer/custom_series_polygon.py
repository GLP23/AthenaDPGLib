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
MAX_RANGE = 1500
MIN_RANGE = -MAX_RANGE

def painter(sender:int|str, app_data:tuple[dict,list,list,Any,Any,Any]):
    """
    A dpg.custom_series painter function to create the proper polygon shape inside the plot.
    The actual shape of the plot doesn't add any functionality other than any visual benefits.
    """
    if landplot_designer_memory.polygons_paused_render:
        return

    # gather all vars we need for the callback
    #   this point is always on 0,0 and 1,1 on the plot
    #   returns the pixel 0,0 and 1,1 would be on
    difference_x = app_data[1][1] - (offset_x :=app_data[1][0])
    difference_y = app_data[2][1] - (offset_y :=app_data[2][0])

    # Delete old polygon's already drawn shapes
    #   And create new shape
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)

    # draw the main shape
    #   and append the first point to the end to "complete" the polygon
    for polygon in landplot_designer_memory.polygons.values(): #type: Polygon
        # assemble the points as
        # If for some reason no points are available
        points = [
            [x,y]
            for _,point in polygon.points
            if MIN_RANGE < (x := ((point[0]*difference_x)+offset_x)) < MAX_RANGE and
               MIN_RANGE < (y := ((point[1]*difference_y)+offset_y)) < MAX_RANGE
        ]

        if len(points) <= 2:
            continue

        dpg.draw_polygon(
            parent=sender,
            points=points,
            fill=polygon.color,
            color=polygon.color,
            thickness=0,
        )

        if polygon.nodes_enabled:
            for point in points:
                dpg.draw_circle(
                    parent=sender,
                    center=point,
                    radius=5,
                    fill=(255,255,255),
                    color=(255,255,255),
                    thickness=0,
                )

    # Always make sure to pop the container stack
    dpg.configure_item(sender, tooltip=False)
    dpg.pop_container_stack()

    dpg.set_value(
        item="render_amount",
        value= len(dpg.get_item_children(sender)[2])
    )
