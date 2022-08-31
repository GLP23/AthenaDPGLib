# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
POLYGONS:int = 10_000 # the amount of polygons to be generated
POLYGON = ((0.,0.),(0.,1.),(1.,1.),(1.,0.)) # shape of the polygon
POLYGON_COLOR = (0,0,0)

MAX_RANGE:float = 750.
MIN_RANGE:float = -MAX_RANGE

polygons:list[tuple] = []
drawn_polygons:list[str|int] = []

# ----------------------------------------------------------------------------------------------------------------------
def custom_series_callback(sender, app_data):
    global drawn_polygons

    # Add mutex here to solve crashing issue
    with dpg.mutex():
        x0 = app_data[1][0]
        y0 = app_data[2][0]
        x1 = app_data[1][1]
        y1 = app_data[2][1]

        difference_x = x1 - x0
        difference_y = y1 - y0

        # delete old drawn items
        #   else we won't update, but simply append to the old image
        #   adding new layers on top of the drawn pieces
        dpg.delete_item(sender, children_only=True)
        dpg.push_container_stack(sender)

        # DO STUFF (maybe threaded calculations in the future?)
        # --------------------------------------------------------------------------------------------------------------
        for polygon in polygons:
            points = calculate_points(polygon,difference_x,difference_y,x0,y0)
            if min(len(points), 3) >= 3:
                drawn_polygons.append(dpg.draw_polygon(
                    points=points,
                    color=POLYGON_COLOR,
                    fill=POLYGON_COLOR,
                    thickness=0
                ))

        # --------------------------------------------------------------------------------------------------------------
        # After everything has been drawn

        dpg.configure_item(sender, tooltip=False)
        dpg.pop_container_stack()

        # Update the text to show the items drawn
        dpg.set_value(
            item="txt_output",
            value=len(dpg.get_item_children(sender, 2))
        )

# ----------------------------------------------------------------------------------------------------------------------
def calculate_points(polygon, difference_x:float, difference_y:float, x0:float, y0:float) -> list[list[float,float]]:
    points = []

    # Calculate all the points in pixel space
    #   don't store any points that are outside the given max range
    for x_original, y_original in polygon:
        if  MIN_RANGE < (x_new := ((x_original * difference_x) + x0)) < MAX_RANGE \
        and MIN_RANGE < (y_new := ((y_original * difference_y) + y0)) < MAX_RANGE:
            points.append([x_new, y_new])

    return points

# ----------------------------------------------------------------------------------------------------------------------
def create_items():
    """
    Function to create the individual items in memory,so they can be drawn to the polygon
    """
    for i in range(POLYGONS):
        polygons.append(
            tuple((x+i,y+i) for x,y in POLYGON)
        )

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    dpg.create_context()
    dpg.create_viewport(title='Plot with large Custom Series Example')

    with dpg.window(tag="primary_window"):
        with dpg.group(horizontal=True, horizontal_spacing=375):
            dpg.add_button(
                label="Create items",
                callback=create_items,
                width=100
            )
            dpg.add_text(tag="txt_output")
        with dpg.plot(width=500, height=500, tag="plot"):
            dpg.add_plot_axis(axis=dpg.mvXAxis)
            with dpg.plot_axis(axis=dpg.mvYAxis):
                dpg.add_custom_series(
                    x= [0.,1.],
                    y= [0.,1.],
                    channel_count=2,
                    callback=custom_series_callback
                )

    dpg.set_primary_window("primary_window", True)

    dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()