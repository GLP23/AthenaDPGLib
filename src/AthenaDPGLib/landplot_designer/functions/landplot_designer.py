# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import itertools
import random
import threading

import dearpygui.dearpygui as dpg
import numpy as np

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.chunk_manager import ChunkManager
from AthenaDPGLib.landplot_designer.models.chunk import Chunk
from AthenaDPGLib.landplot_designer.models.land_plot import LandPlot
from AthenaDPGLib.landplot_designer.models.coordinate import Coordinate
from AthenaDPGLib.landplot_designer.functions.plot_custom_series import custom_series_callback

from AthenaDPGLib.landplot_designer.data.polygon_shapes import (
    SQUARE, RECTANGLE, HEXAGON,HEXAGON_BIG,HEXAGON_HUGE, HEXAGON_IMMENSE, HEXAGON_COLOSSAL
)

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
POLYGON = ((0.,0.),(0.,1.),(1.,1.),(1.,0.)) # shape of the polygon
CHUNK_SIDE_LENGTH = 16
SHAPES = (SQUARE,RECTANGLE,HEXAGON)

chunk_manager:ChunkManager = ChunkManager()
old_mouse_pos_plot_space:np.ndarray = np.array((0., 0.))

def create_items():
    """
    Function to create the individual items in memory,so they can be drawn to the polygon
    """
    global chunk_manager

    print("started")

    for i in range(10_000):
        modifier_x = random.randint(-1_000,1_000)
        modifier_y = random.randint(-1_000,1_000)

        chunk_manager.add_land_plot(
            land_plot=LandPlot(
                points=[
                    Coordinate(x+modifier_x,y+modifier_y)
                    for x,y in random.choice(SHAPES)
                ],
                color=(255,255,255)
            )
        )

    print("finished")
    print(len(list(chunk_manager.chunks)))

    update_renderable()

def update_renderable():
    global chunk_manager,old_mouse_pos_plot_space
    x_limit0, x_limit1 = dpg.get_axis_limits("x_axis")
    y_limit0, y_limit1 = dpg.get_axis_limits("y_axis")

    chunk_manager.renderable_update(
        TL_limit=np.array([x_limit0, y_limit0]) + chunk_manager.offset,
        BR_limit=np.array([x_limit1, y_limit1]) + chunk_manager.offset
    )

def update_drag():
    global chunk_manager,old_mouse_pos_plot_space
    if dpg.is_mouse_button_dragging(dpg.mvMouseButton_Left, threshold=0.1):
        with dpg.mutex():
            pos_plot_space = np.array(dpg.get_plot_mouse_pos())

            if old_mouse_pos_plot_space.all() != np.array((0., 0.)).all() :
                chunk_manager.offset -= old_mouse_pos_plot_space - pos_plot_space

            old_mouse_pos_plot_space = pos_plot_space

    update_renderable()



def update_drag_clicked():
    global chunk_manager,old_mouse_pos_plot_space
    old_mouse_pos_plot_space = np.array((0., 0.))

    update_renderable()


def registry():
    with dpg.item_handler_registry(tag="registry"):
        dpg.add_item_visible_handler(
            callback=update_drag
        )
        dpg.add_item_clicked_handler(
            callback=update_drag_clicked
        )
    dpg.bind_item_handler_registry(
        handler_registry="registry",
        item="plot"
    )

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    global chunk_manager

    dpg.create_context()
    dpg.create_viewport(title='Plot with large Custom Series Example')

    with dpg.window(tag="primary_window"):
        with dpg.group(horizontal=True, horizontal_spacing=50):
            dpg.add_button(
                label="Create items",
                callback=lambda : (threading.Thread(target=create_items).start()),
                width=100
            )
            dpg.add_text(tag="txt_output_chunks")
            dpg.add_text(tag="txt_output_polygons")
        with dpg.plot(width=750, height=750, tag="plot", callback=update_renderable,anti_aliased=True):
            dpg.add_plot_axis(tag="x_axis",axis=dpg.mvXAxis)
            with dpg.plot_axis(tag="y_axis", axis=dpg.mvYAxis):
                dpg.add_custom_series(
                    x= (xy:=[0.,1.]),
                    y= xy,
                    channel_count=2,
                    callback=custom_series_callback,
                    user_data=chunk_manager
                )

    dpg.set_axis_limits("x_axis", -10,10)
    dpg.set_axis_limits("y_axis", -10,10)
    dpg.set_primary_window("primary_window", True)
    registry()

    # dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()