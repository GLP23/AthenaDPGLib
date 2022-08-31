# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.fixes.mutex import run_in_mutex
from AthenaDPGLib.landplot_designer.models.polygons import ChunkOfPolygons

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
MAX_RANGE:float = 750.
MIN_RANGE:float = -MAX_RANGE

@run_in_mutex
def custom_series_callback(sender, app_data, polygons:ChunkOfPolygons):
    x0 = app_data[1][0]
    y0 = app_data[2][0]
    x1 = app_data[1][1]
    y1 = app_data[2][1]

    difference_point = (x1 - x0, y1 - y0)
    zero_point = (x0,y0)

    # delete old drawn items
    #   else we won't update, but simply append to the old image
    #   adding new layers on top of the drawn pieces
    dpg.delete_item(sender, children_only=True)
    dpg.push_container_stack(sender)

    # DO STUFF (maybe threaded calculations in the future?)
    # --------------------------------------------------------------------------------------------------------------
    for polygon in polygons.renderable_get():
        # if len(coords) >= 3:
        dpg.draw_polygon(
            points=[coord.output_to_pixelspace(difference_point, zero_point) for coord in polygon.coords],
            color=polygon.color,
            fill=polygon.color,
            thickness=0
        )

    # --------------------------------------------------------------------------------------------------------------
    # After everything has been drawn

    dpg.configure_item(sender, tooltip=False)
    dpg.pop_container_stack()

    # Update the text to show the items drawn
    dpg.set_value(
        item="txt_output",
        value=len(dpg.get_item_children(sender, 2))
    )

    # Update the text to show the items drawn
    # print(f"children: {len(dpg.get_item_children(sender, 2))}")