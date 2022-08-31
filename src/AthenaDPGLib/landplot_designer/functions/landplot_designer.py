# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import random
import threading

import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygons import Polygon, Coordinate, ChunkOfPolygons
from AthenaDPGLib.landplot_designer.functions.plot_custom_series import custom_series_callback

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
polygons:ChunkOfPolygons = ChunkOfPolygons()
POLYGON = ((0.,0.),(0.,1.),(1.,1.),(1.,0.)) # shape of the polygon
SHAPE = 100

x_limit0, x_limit1 = 0.,0.
y_limit0, y_limit1 = 0.,0.

def create_items():
    """
    Function to create the individual items in memory,so they can be drawn to the polygon
    """
    global polygons

    print("started")
    polygons.clear()

    for a in range(SHAPE):
        for b in range(SHAPE):
            # noinspection PyArgumentList
            polygons.append(Polygon(
                coords=[
                    Coordinate(x + a, y + b)
                    for x, y in POLYGON
                ],
                color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            ))

    print("finished")

def update_renderable():
    global polygons, x_limit0, x_limit1 ,y_limit0, y_limit1

    with dpg.mutex():
        for polygon in polygons.collection:
            polygon.renderable_update(
                x_limit0, x_limit1, y_limit0, y_limit1
            )

def get_plot_limits():
    global x_limit0, x_limit1 ,y_limit0, y_limit1

    x_limit0, x_limit1 = dpg.get_axis_limits("x_axis")
    y_limit0, y_limit1 = dpg.get_axis_limits("y_axis")

def registry():
    with dpg.item_handler_registry(tag="registry"):
        dpg.add_item_visible_handler(
            callback=update_renderable
        )
        dpg.add_item_hover_handler(
            callback=get_plot_limits
        )
    dpg.bind_item_handler_registry(
        handler_registry="registry",
        item="plot"
    )

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    global polygons

    dpg.create_context()
    dpg.create_viewport(title='Plot with large Custom Series Example')

    with dpg.window(tag="primary_window"):
        with dpg.group(horizontal=True, horizontal_spacing=375):
            dpg.add_button(
                label="Create items",
                callback=lambda : (threading.Thread(target=create_items).start()),
                width=100
            )
            dpg.add_text(tag="txt_output")
        with dpg.plot(width=500, height=500, tag="plot", callback=update_renderable):
            dpg.add_plot_axis(tag="x_axis",axis=dpg.mvXAxis)
            with dpg.plot_axis(tag="y_axis", axis=dpg.mvYAxis):
                dpg.add_custom_series(
                    x= (xy:=[0.,1.]),
                    y= xy,
                    channel_count=2,
                    callback=custom_series_callback,
                    user_data=polygons
                )

    get_plot_limits()

    dpg.set_primary_window("primary_window", True)
    registry()

    dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()