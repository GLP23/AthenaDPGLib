# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import ClassVar

# Custom Library
from AthenaLib.data.types import PATHLIKE

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class WndLandplotDesigner:
    plot_name:ClassVar[str] = "plot_landplot_designer"
    series_polygon: ClassVar[str] = "series_polygon"
    window_tag:str

    def __init__(self, background_path: PATHLIKE, window_tag:str):

        # Define the background texture and assign it to the window
        width, height, channels, data = dpg.load_image(background_path)
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="background_id")

        self.window_tag = window_tag
        self.polygons = []

    def define_dpg(self):
        with dpg.window(tag=self.window_tag):
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()

                with dpg.table_row():
                    with dpg.group():
                        with dpg.group(horizontal=True):
                            dpg.add_input_text(tag="polygon_name")
                            dpg.add_button(
                                label="define polygon",
                                callback=self.btn_define_polygon,
                            )

                        with dpg.table(tag="tbl_polygons", scrollY=True, height=500):
                            dpg.add_table_column(label="name")
                            dpg.add_table_column(label="select")
                            dpg.add_table_column(label="color")
                            dpg.add_table_column(label="points")

                    with dpg.plot(tag=self.plot_name, width=500, height=500):
                        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
                        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
                        # define custom series to handle the polygon shapes

            with dpg.group(horizontal=True):
                dpg.add_text("selected polygon:")
                dpg.add_text(tag="poly_selected")

            dpg.add_button(label="make polygons", callback=self.update_polygon_all)

        with dpg.item_handler_registry(tag="ireg_0"):
            dpg.add_item_clicked_handler(
                callback=lambda: self.plot_mouse_click_callback()
            )

        dpg.bind_item_handler_registry(self.plot_name, "ireg_0")


    def btn_define_polygon(self):
        polyname = dpg.get_value("polygon_name")

        for child in dpg.get_item_children("tbl_polygons")[1]:
            if dpg.get_item_alias(child) == f"row_{polyname}":
                print("ERROR")
                break

        else:
            with dpg.table_row(tag=f"row_{polyname}", parent="tbl_polygons", user_data=polyname):
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

    def gather_polygon_points(self, point_tags: list[{str}]):
        x_data = []
        y_data = []
        for p in point_tags:
            x, y, *_ = dpg.get_value(int(p))
            x_data.append(x)
            y_data.append(y)
        return x_data, y_data

    def update_polygon(self,_,__, user_data:str):
        polyname = user_data
        if not (points_str := dpg.get_value(f'points_{polyname}')):
            return
        if len(point_tags := points_str.split(";")) <= 2:
            return
        x_data, y_data = self.gather_polygon_points(point_tags)
        if len(x_data) != len(dpg.get_value(f'series_{polyname}')[0]):
            return
        dpg.set_value(f'series_{polyname}', [x_data, y_data])


    def update_polygon_all(self):
        for row in dpg.get_item_children("tbl_polygons")[1]:
            polyname = dpg.get_item_user_data(row)

            if not (points_str := dpg.get_value(f'points_{polyname}')):
                return

            if len(point_tags := points_str.split(";")) <= 2:
                return

            x_data, y_data = self.gather_polygon_points(point_tags)

            if dpg.does_item_exist(f'series_{polyname}'):
                if len(x_data) == len(dpg.get_value(f'series_{polyname}')[0]):
                    dpg.set_value(f'series_{polyname}', [x_data, y_data])
                else:
                    dpg.delete_item(f'series_{polyname}')
                    dpg.add_custom_series(
                        x_data, y_data,
                        2,
                        parent="x_axis",
                        callback=self.series_polygon_callback,
                        tag=f'series_{polyname}',
                    )

            else:
                dpg.add_custom_series(
                    x_data, y_data,
                    2,
                    parent="x_axis",
                    callback=self.series_polygon_callback,
                    tag=f'series_{polyname}',
                )

    def series_polygon_callback(self, sender, app_data):
        _helper_data = app_data[0]

        transformed_x = app_data[1]
        transformed_y = app_data[2]

        # print(transformed_x,transformed_y)

        dpg.delete_item(sender, children_only=True, slot=2)
        dpg.push_container_stack(sender)
        dpg.configure_item(sender, tooltip=False)


        dpg.draw_polygon(
            points=[[x,y] for x,y in zip(transformed_x, transformed_y)],
            fill=(255,255,255, 255),
            thickness=0
        )

        dpg.pop_container_stack()

    def plot_mouse_click_callback(self):
        if not (polyname := dpg.get_value("poly_selected")): # if truthy
            return
        pos = dpg.get_plot_mouse_pos()
        point = dpg.add_drag_point(
            parent=self.plot_name,
            default_value=pos,
            color=dpg.get_value(f"color_{polyname}"),
            callback=self.update_polygon,
            user_data=polyname
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
