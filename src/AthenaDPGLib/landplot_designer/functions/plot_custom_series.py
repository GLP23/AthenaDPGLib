# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.fixes.mutex import run_in_mutex
from AthenaDPGLib.landplot_designer.models.chunk_manager import ChunkManager
from AthenaDPGLib.landplot_designer.models.land_plot import LandPlot
from AthenaDPGLib.landplot_designer.models.chunk import Chunk

from AthenaDPGLib.landplot_designer.functions.pixelspace_conversions import coord_to_pixelspace

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@run_in_mutex
def custom_series_callback(sender, app_data, chunk_manager:ChunkManager):
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
    for chunk in chunk_manager.renderable_get(): #type: Chunk
        dpg.draw_polygon(
            points=[
                coord_to_pixelspace(coord, difference_point, zero_point)
                for coord in chunk.points
            ],
            color=(127,157,35),
            fill=(127,157,35),
            thickness=0
        )

        for land_plot in chunk.land_plots: #type: LandPlot
            # if len(points) >= 3:
            dpg.draw_polygon(
                points=[
                    coord_to_pixelspace(coord, difference_point, zero_point)
                    for coord in land_plot.points
                ],
                color=land_plot.color,
                fill=land_plot.color,
                thickness=0
        )

    # --------------------------------------------------------------------------------------------------------------
    # After everything has been drawn

    dpg.configure_item(sender, tooltip=False)
    dpg.pop_container_stack()

    # Update the text to show the items drawn
    dpg.set_value(
        item="txt_output_chunks",
        value=f"chunks: {len(list(chunk_manager.renderable_get()))}"
    )
    dpg.set_value(
        item="txt_output_polygons",
        value=f"polygons: {len(dpg.get_item_children(sender, 2))}"
    )

    # Update the text to show the items drawn
    # print(f"children: {len(dpg.get_item_children(sender, 2))}")