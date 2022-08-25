# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.data.types import PATHLIKE

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def mouse_press_callback(_,__,___):
    if not (polyname := dpg.get_value("poly_selected")): # if truthy
        return
    pos = dpg.get_plot_mouse_pos()
    point = dpg.add_drag_point(
        parent="plot_1",
        default_value=pos,
        color=dpg.get_value(f"color_{polyname}")
    )
    val = dpg.get_value(f'points_{polyname}')
    dpg.set_value(
        item=f"points_{polyname}",
        value=f"{val};{point}" if val else f"{point}"
    )

def selected_polygon(_,app_data,userdata:str):
    if app_data:
        dpg.set_value("poly_selected", userdata)
        for row in dpg.get_item_children("tbl_polygons")[1]:
            if dpg.get_item_alias(row) == f"row_{userdata}":
                continue

            checkbox = dpg.get_item_children(row)[1][1]
            dpg.set_value(checkbox, False)
    else:
        dpg.set_value("poly_selected", "")

def btn_define_polygon(_, __,user_data:str):
    polyname = dpg.get_value(user_data)

    for child in dpg.get_item_children("tbl_polygons")[1]:
        if dpg.get_item_alias(child) == f"row_{polyname}":
            print("ERROR")
            break

    else:
        with dpg.table_row(tag=f"row_{polyname}", parent="tbl_polygons"):
            dpg.add_text(default_value=polyname)
            dpg.add_checkbox(
                tag=f"cbox_{polyname}",
                user_data=polyname,
                callback=selected_polygon
            )
            dpg.add_color_button(tag=f"color_{polyname}")
            dpg.add_text(tag=f"points_{polyname}")

        dpg.set_value(f"cbox_{polyname}", True)
        dpg.set_value("poly_selected", polyname)

def custom_series_polygon(sender, app_data, user_data):
    _helper_data = app_data[0]
    transformed_x = app_data[1]
    transformed_y = app_data[2]
    mouse_x_plot_space = _helper_data["MouseX_PlotSpace"]
    mouse_y_plot_space = _helper_data["MouseY_PlotSpace"]
    mouse_x_pixel_space = _helper_data["MouseX_PixelSpace"]
    mouse_y_pixel_space = _helper_data["MouseY_PixelSpace"]
    dpg.delete_item(sender, children_only=True, slot=2)
    dpg.push_container_stack(sender)
    dpg.configure_item(user_data["name"], tooltip=False)

    dpg.draw_polygon(
        points=[[x,y]for x, y in zip(transformed_x,transformed_y)],
        fill=user_data["color"],
        thickness=2
    )

    dpg.pop_container_stack()

def generate_polygon(_,__):
    for i, child in enumerate(dpg.get_item_children("tbl_polygons")[1]):
        polyname = dpg.get_item_alias(child).split("_")[-1]

        x_data = []
        y_data = []

        for p in [int(p) for p in dpg.get_value(f'points_{polyname}').split(";")]:
            x, y, *_ = dpg.get_value(p)
            x_data.append(x)
            y_data.append(y)

        with dpg.custom_series(
                x_data,
                y_data,
                2,
                parent="x_axis",
                callback=custom_series_polygon,
                user_data={
                    "name": f'custom_series_{polyname}',
                    "color": (i*50, i*50, i*50)
                },
                tag=f'custom_series_{polyname}'
        ):
            pass


def wnd_landplot_designer(background_path:PATHLIKE):
    # Define the background texture and assign it to the window
    width, height, channels, data = dpg.load_image(background_path)
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="background_id")

    with dpg.item_handler_registry(tag="ireg_0"):
        dpg.add_item_clicked_handler(callback=mouse_press_callback)

    with dpg.window(tag="wnd_landplot_designer"):

        # ability to define new polygroup
        with dpg.group(horizontal=True):
            dpg.add_input_text(tag="polygon_name")
            dpg.add_button(
                label="define polygon",
                callback=btn_define_polygon,
                user_data="polygon_name"
            )

        with dpg.table(tag="tbl_polygons"):
            dpg.add_table_column(label="name")
            dpg.add_table_column(label="select")
            dpg.add_table_column(label="color")
            dpg.add_table_column(label="points")

        with dpg.group(horizontal=True):
            dpg.add_text("selected polygon:")
            dpg.add_text(tag="poly_selected")

        with dpg.plot(tag="plot_1"):
            dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

        dpg.add_button(label="generate polygon", callback=generate_polygon)

    dpg.bind_item_handler_registry("plot_1", "ireg_0")