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
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
# a global storage of the individual points on the plot.
#   This list holds the dpg tags of the dragpoints, and not the individual positions
#   If you want to have a list of all points' postions at a specific moment
#       you'll need to exectute the points_as_positions functions
points:list[int] = []

def points_as_pos(list_of_points:list[int]):
    return [dpg.get_value(p)[:2] for p in list_of_points]

def plot_mouseclick_left_callback():
    global points

    # retrieve the current mouse postion
    #   and create point
    pos = dpg.get_plot_mouse_pos()
    point = dpg.add_drag_point(
        parent="plot",
        default_value=pos,
        callback=lambda : print("Point dragged"), # this callback is executed on dragging dragpoint
    )

    # After the point has been created
    #   Store the point tag somewhere (in this case auto generated)
    #   This way the point can be easily retrieved later
    points.append(point)

def plot_mouseclick_right_callback():
    global points

    # Use numpy to find the nearest point through a simple algorithm
    pos = dpg.get_plot_mouse_pos()
    index_nearest = np.argmin(np.sum((np.asarray(points_as_pos(points)) - pos) ** 2, axis=1))

    # Delete the item from the plot and from the stored values
    #   Make sure to delete the removed point from the list of points as well
    dpg.delete_item(points[index_nearest])
    points.pop(index_nearest)

# ----------------------------------------------------------------------------------------------------------------------
# - Main Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    """
    A simple example of how to set up a drag point handler for a plot
    The handler makes it so that:
    - on a left click on the plot, it will create a drag point
    - on a right click on the plot, it will delete the nearest drag point
    """
    dpg.create_context()
    dpg.create_viewport(title='Dragpoint Example')

    # Create a simple layout that has a plot within it
    #   Make sure to store the plot tag somwhere
    #       or use a custom tag as with this example
    with dpg.window(label="Plot with dragpoints"):
        dpg.add_plot(tag="plot", width=500, height=500, no_menus=True)

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