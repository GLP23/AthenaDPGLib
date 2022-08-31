# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import numpy as np

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygons import Polygon, Point
from AthenaDPGLib.landplot_designer.functions.plot_custom_series import custom_series_callback

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
polygons:set[Polygon] = set()
POLYGON = ((0.,0.),(0.,1.),(1.,1.),(1.,0.)) # shape of the polygon

def create_items():
    """
    Function to create the individual items in memory,so they can be drawn to the polygon
    """
    global polygons

    polygons.clear()

    for i in range(10_000):
        # noinspection PyArgumentList
        polygons.add(
            Polygon(
                points=tuple(
                    Point(x+i,y+i)
                    for x, y in POLYGON
                )
            )
        )

def test():
    global polygons

    x_limit0, x_limit1 = dpg.get_axis_limits("x_axis")
    y_limit0, y_limit1 = dpg.get_axis_limits("y_axis")

    for polygon in polygons:

        x,y = (
            np.array([point[0] for point in polygon.points]).sum()/(length := len(polygon.points)),
            np.array([point[1] for point in polygon.points]).sum()/length
        )

        polygon.do_render = x_limit0 < x < x_limit1 or y_limit0 < y < y_limit1

def registry():
    with dpg.item_handler_registry(tag="registry"):
        # dpg.add_item_clicked_handler(
        #     callback=test
        # )
        dpg.add_item_active_handler(
            callback=test
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
                callback=create_items,
                width=100
            )
            dpg.add_button(
                label="test",
                callback=test,
                width=100
            )
            dpg.add_text(tag="txt_output")
        with dpg.plot(width=500, height=500, tag="plot", callback=test):
            dpg.add_plot_axis(tag="x_axis",axis=dpg.mvXAxis)
            with dpg.plot_axis(tag="y_axis", axis=dpg.mvYAxis):
                dpg.add_custom_series(
                    x= [0.,1.],
                    y= [0.,1.],
                    channel_count=2,
                    callback=custom_series_callback,
                    user_data=polygons
                )

    dpg.set_primary_window("primary_window", True)
    registry()

    dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()