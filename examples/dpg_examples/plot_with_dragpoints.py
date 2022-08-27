# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import numpy as np

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
points:list[int] = []

def plot_mouseclick_left_callback():
    global points

    # retrieve the current mouse postion
    #   and create point
    pos = dpg.get_plot_mouse_pos()
    point = dpg.add_drag_point(
        parent="plot",
        default_value=pos,
        callback=lambda : print("Point Clicked"),
    )
    # After the point has been created
    #   Store the point tag somewhere (in this case auto generated)
    #   This way the point can be easily retrieved later
    points.append(point)

def plot_mouseclick_right_callback():
    global points
    # Use numpy to find the nearest point through a simple algorithm
    pos = dpg.get_plot_mouse_pos()
    index_nearest = np.argmin(np.sum((np.asarray([dpg.get_value(p)[:2] for p in points]) - pos)**2, axis=1))

    # Delete the item from the plot and from the stored values
    #   Make sure to delete the removed point from the list of points as well
    dpg.delete_item(points[index_nearest])
    points.pop(index_nearest)

def main():
    dpg.create_context()
    dpg.create_viewport(title='Dragpoint Example')

    # Create a simple layout that has a plot within it
    #   Make sure to store the plot tag somwhere
    #       or use a custom tag as with this example
    with dpg.window(label="Plot with dragpoints"):
        with dpg.plot(tag="plot", width=500, height=500, no_menus=True, ):
            dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

    # Create a registry for the different callbacks on different mouse button clicks
    with dpg.item_handler_registry(tag="registry"):
        # Callback system for when the user left-clicks on the plot
        dpg.add_item_clicked_handler(
            button=dpg.mvMouseButton_Left,
            callback=plot_mouseclick_left_callback
        )
        # Callback system for when the user right-clicks on the plot
        dpg.add_item_clicked_handler(
            button=dpg.mvMouseButton_Right,
            callback=plot_mouseclick_right_callback
        )

    # bind the registry to the item
    dpg.bind_item_handler_registry("plot", "registry")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()