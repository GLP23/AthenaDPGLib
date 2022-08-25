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
from AthenaDPGLib.functions.custom_dpg_functions import grid_layout

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class WndLandplotDesigner:
    plot_name:ClassVar[str] = "plot_landplot_designer"
    series_polygon: ClassVar[str] = "series_polygon"
    window_tag:str
    ireg_node_callback:ClassVar[str] = "ireg_node_callback"

    def __init__(self, background_path: PATHLIKE, window_tag:str):
        # Define the background texture and assign it to the window
        width, height, channels, data = dpg.load_image(background_path)
        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="background_id")

        self.window_tag = window_tag

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        self.define_dpg()
        self.define_registries()

    # ------------------------------------------------------------------------------------------------------------------
    def define_dpg(self):
        """
        Defines the general dpg structure which is loaded when the window is created
        """
        with dpg.window(tag=self.window_tag):
            with grid_layout(columns=3, policy=dpg.mvTable_SizingStretchProp):
                with dpg.table_row():
                    # col 1 : PLOT and general working area
                    with dpg.plot(tag=self.plot_name, width=500, height=500):
                        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
                        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
                        # define custom series to handle the polygon shapes

                    # col 2 : Tools and windows for editing PLOT
                    with dpg.group():
                        dpg.add_button(label="make polygons", callback=self.update_polygon_all)

                        with dpg.group(horizontal=True):
                            dpg.add_text("selected:")
                            dpg.add_text(tag="poly_selected")

                    # col 3 : polygon groups and setup of the polygons
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

    # ------------------------------------------------------------------------------------------------------------------
    def define_registries(self):
        """
        A place to define all registries with their corresponding actions:
        """
        # Registry for the entire plot
        with dpg.item_handler_registry(tag="ireg_0"):
            dpg.add_item_clicked_handler(
                callback=self.plot_mouse_click_callback
            )

        # Bind all the registries that can be used
        dpg.bind_item_handler_registry(self.plot_name, "ireg_0")

    # ------------------------------------------------------------------------------------------------------------------
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
                    callback=self.selected_polygon
                )
                dpg.add_color_edit(tag=f"color_{polyname}", width=250, no_inputs=True)

                # with dpg.popup(parent=dpg.last_item()):
                #     dpg.add_color_picker(
                #         callback=lambda sender, app_data: dpg.set_value(f"color_{polyname}", app_data)
                #     )

                dpg.add_text(tag=f"points_{polyname}")

            dpg.set_value(f"cbox_{polyname}", True)
            dpg.set_value("poly_selected", polyname)

    def update_polygon(self,polyname:str):
        # check as soon as possible if the polygon is actually creatable
        if not (points_str := dpg.get_value(f'points_{polyname}')):
            return
        if len(point_tags := points_str.split(";")) <= 2:
            return

        # assemble all the points
        #   todo offload this unpacking to the stored values in the column
        x_data = [dpg.get_value(int(p))[0] for p in point_tags]
        y_data = [dpg.get_value(int(p))[1] for p in point_tags]

        # create a new polygon if it doesn't exsist yet
        if not dpg.does_item_exist(f'series_{polyname}'):
            self.create_new_polygon(x_data, y_data, polyname)

        elif len(x_data) == len(dpg.get_value(f'series_{polyname}')[0]):
            dpg.set_value(f'series_{polyname}', [x_data, y_data])

        else:
            # this assumes that the node count in the polygon has changed
            #   And allows us to delete the old one and create a new polygon
            dpg.delete_item(f'series_{polyname}')
            self.create_new_polygon(x_data, y_data, polyname)

    def create_new_polygon(self, x_data, y_data, polyname):
        dpg.add_custom_series(
            x_data, y_data,
            2,
            parent="x_axis",
            callback=self.series_polygon_callback,
            tag=f'series_{polyname}',
            user_data=polyname
        )

    def update_polygon_all(self):
        for row in dpg.get_item_children("tbl_polygons")[1]:
            self.update_polygon(polyname=dpg.get_item_user_data(row))

    def series_polygon_callback(self, sender, app_data, user_data):
        # gather all vars we need for the callback
        transformed_x = app_data[1]
        transformed_y = app_data[2]
        polyname = user_data

        # Delete old polygon and create new items
        dpg.delete_item(sender, children_only=True, slot=2)
        dpg.push_container_stack(sender)
        # dpg.configure_item(sender, tooltip=False)

        # draw the main shape
        points = [[x,y] for x,y in zip(transformed_x, transformed_y)]
        points.append(points[0])
        color = dpg.get_value(f"color_{polyname}")
        dpg.draw_polygon(
            points=points,
            color=color,
            fill=color,
            thickness=0
        )

        # draw the points afterwards
        #   If this is done first, these will come behind the polygon, which is not what we want
        for point in zip(transformed_x, transformed_y):
            dpg.draw_circle(point, radius=5, fill=(0,0,0))

        # Always make sure to pop the container stack
        dpg.pop_container_stack()

    def plot_mouse_click_callback(self):
        if not (polyname := dpg.get_value("poly_selected")): # if truthy
            return

        pos = dpg.get_plot_mouse_pos()
        point = dpg.add_drag_point(
            parent=self.plot_name,
            default_value=pos,
            color=dpg.get_value(f"color_{polyname}"),
            callback=lambda _,__, user_data: self.update_polygon(user_data),
            user_data=polyname
        )
        val = dpg.get_value(f'points_{polyname}')
        dpg.set_value(
            item=f"points_{polyname}",
            value=f"{val};{point}" if val else f"{point}"
        )

        self.update_polygon_all()

    def custom_node_callback(self, sender, app_data, user_data):
        print(sender, app_data, user_data)
        if dpg.is_mouse_button_clicked(button=1):
            print("right clicked")
        else:
            print("here")

    def selected_polygon(self, _,app_data,userdata:str):
        if app_data:
            dpg.set_value("poly_selected", userdata)
            for row in dpg.get_item_children("tbl_polygons")[1]:
                if dpg.get_item_alias(row) == f"row_{userdata}":
                    continue

                dpg.set_value(dpg.get_item_children(row)[1][1], False)
        else:
            dpg.set_value("poly_selected", "")
