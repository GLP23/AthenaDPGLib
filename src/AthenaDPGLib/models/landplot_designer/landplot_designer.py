# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import ClassVar
import numpy as np
import math

# Custom Library
from AthenaLib.data.types import PATHLIKE
from AthenaLib.functions.nearest_point import closest_point_index

# Custom Packages
from AthenaDPGLib.models.landplot_designer.polygon import Polygon
from AthenaDPGLib.functions.custom_dpg_functions import grid_layout

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class WndLandplotDesigner:
    plot_name:ClassVar[str] = "plot_landplot_designer"
    series_polygon: ClassVar[str] = "series_polygon"
    window_tag:str
    ireg_node_callback:ClassVar[str] = "ireg_node_callback"
    polygons:dict[str:Polygon]

    def __init__(self, background_path: PATHLIKE, window_tag:str):
        # Define the background texture and assign it to the window
        # width, height, channels, data = dpg.load_image(background_path)
        # with dpg.texture_registry():
        #     dpg.add_static_texture(width, height, data, tag="background_id")

        self.window_tag = window_tag
        self.polygons = {}

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
            with grid_layout(columns=2, policy=dpg.mvTable_SizingStretchProp):
                with dpg.table_row():
                    # col 1 : PLOT and general working area
                    with dpg.plot(tag=self.plot_name, width=500, height=500, no_menus=True,):
                        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
                        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
                        # define custom series to handle the polygon shapes

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

                with dpg.table_row():
                    # col 1 :
                    with dpg.group(horizontal=True):
                        with dpg.group(horizontal=True):
                            dpg.add_text("selected:")
                            dpg.add_text(tag="poly_selected")
                        with dpg.group(horizontal=True):
                            dpg.add_button(
                                label = "print polygons",
                                callback=lambda :print(self.polygons)
                            )
                    # col 2 :
                    # /

    # ------------------------------------------------------------------------------------------------------------------
    def define_registries(self):
        """
        A place to define all registries with their corresponding actions:
        """
        # Registry for the entire plot
        with dpg.item_handler_registry(tag="ireg_0"):
            dpg.add_item_clicked_handler(
                button=dpg.mvMouseButton_Left,
                callback=self.plot_mouseclick_left_callback,
            )
            dpg.add_item_clicked_handler(
                button=dpg.mvMouseButton_Right,
                callback=self.plot_mouseclick_right_callback
            )

        # Bind all the registries that can be used
        dpg.bind_item_handler_registry(self.plot_name, "ireg_0")

    # ------------------------------------------------------------------------------------------------------------------
    def btn_define_polygon(self):
        polygon = Polygon(
            name=dpg.get_value("polygon_name"),
        )

        for child in dpg.get_item_children("tbl_polygons")[1]:
            if dpg.get_item_alias(child) == f"row_{polygon.name}":
                print("ERROR")
                break

        else:
            with dpg.table_row(tag=f"row_{polygon.name}", parent="tbl_polygons", user_data=polygon.name):
                dpg.add_text(default_value=polygon.name)
                dpg.add_checkbox(
                    tag=f"cbox_{polygon.name}",
                    user_data=polygon.name,
                    callback=self.selected_polygon
                )
                dpg.add_color_edit(
                    tag=f"color_{polygon.name}",
                    width=250,
                    no_inputs=True,
                    callback=lambda _,__, pg: setattr(pg, "color", dpg.get_value(f"color_{pg.name}")),
                    user_data=polygon
                )

            dpg.set_value(f"cbox_{polygon.name}", True)
            dpg.set_value("poly_selected", polygon.name)

        self.polygons[polygon.name] = polygon

    def update_polygon(self,polyname:str):
        # check as soon as possible if the polygon is actually creatable
        if (polyname not in self.polygons) or (len((points := self.polygons[polyname].points)) <= 2):
            return

        # assemble all the points
        #   todo offload this unpacking to the stored values in the column
        x_data = [dpg.get_value(p)[0] for p in points]
        y_data = [dpg.get_value(p)[1] for p in points]

        # create a new polygon if it doesn't exsist yet
        if not dpg.does_item_exist(f'series_{polyname}'):
            self.create_new_polygon_series(x_data, y_data, polyname)

        elif len(x_data) == len(dpg.get_value(f'series_{polyname}')[0]):
            dpg.set_value(f'series_{polyname}', [x_data, y_data])

        else:
            # this assumes that the node count in the polygon has changed
            #   And allows us to delete the old one and create a new polygon
            dpg.delete_item(f'series_{polyname}')
            self.create_new_polygon_series(x_data, y_data, polyname)

    def create_new_polygon_series(self, x_data, y_data, polyname):
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
        # fixes an issue that relates to quickly redrawing the series
        if not dpg.does_item_exist(sender):
            return

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

    def plot_mouseclick_left_callback(self):
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

        self.polygons[polyname].points.append(point)

        self.update_polygon(polyname=polyname)

    def plot_mouseclick_right_callback(self):
        if not (polyname := dpg.get_value("poly_selected")):  # if truthy
            return

        polygon: Polygon = self.polygons[polyname]

        if dpg.is_key_down(dpg.mvKey_Alt):
            pos = dpg.get_plot_mouse_pos()
            point = dpg.add_drag_point(
                parent=self.plot_name,
                default_value=pos,
                color=dpg.get_value(f"color_{polyname}"),
                callback=lambda _, __, user_data: self.update_polygon(user_data),
                user_data=polyname
            )
            points = [dpg.get_value(point)[:2] for point in polygon.points]
            index = closest_point_index(point=pos, points=points)

            x,y, *_ = pos
            x_origin, y_origin, *_ = dpg.get_value(polygon.points[index])
            if index == 0:
                x_origin_prev, y_origin_prev, *_ = dpg.get_value(polygon.points[-1])
            else:
                x_origin_prev, y_origin_prev, *_ = dpg.get_value(polygon.points[index-1])

            match x_origin-x_origin_prev,y_origin-y_origin_prev:
                # first Quadrant
                case x__, y__ if x__>0 and y__>0:
                    match (x - x_origin, y - y_origin):
                        # first Quadrant
                        case x_, y_ if x_ > 0 and y_ > 0:
                            index = index+1
                        # second Quadrant
                        case x_, y_ if x_ < 0 and y_ > 0:
                            index = index
                        # third Quadrant
                        case x_, y_ if x_ < 0 and y_ < 0:
                            index = index
                        # fourth Quadrant
                        case x_, y_ if x_ > 0 and y_ < 0:
                            index = index+1
                        # origin
                        case x_, y_ if x_ == 0 and y_ == 0:
                            pass
                        # x axis positive
                        case x_, y_ if x_ > 0 and y_ == 0:
                            index = index+1
                        # x axis negative
                        case x_, y_ if x_ < 0 and y_ == 0:
                            index = index
                        # y axis positive
                        case x_, y_ if x_ == 0 and y_ > 0:
                            index = index
                        # y axis negative
                        case x_, y_ if x_ == 0 and y_ < 0:
                            index = index
                # second Quadrant
                case x__, y__ if x__<0 and y__>0:
                    match (x - x_origin, y - y_origin):
                        # first Quadrant
                        case x_, y_ if x_ > 0 and y_ > 0:
                            index = index+1
                        # second Quadrant
                        case x_, y_ if x_ < 0 and y_ > 0:
                            index = index+1
                        # third Quadrant
                        case x_, y_ if x_ < 0 and y_ < 0:
                            index = index
                        # fourth Quadrant
                        case x_, y_ if x_ > 0 and y_ < 0:
                            index = index
                        # origin
                        case x_, y_ if x_ == 0 and y_ == 0:
                            pass
                        # x axis positive
                        case x_, y_ if x_ > 0 and y_ == 0:
                            index = index+1
                        # x axis negative
                        case x_, y_ if x_ < 0 and y_ == 0:
                            index = index
                        # y axis positive
                        case x_, y_ if x_ == 0 and y_ > 0:
                            index = index
                        # y axis negative
                        case x_, y_ if x_ == 0 and y_ < 0:
                            index = index+1
                # third Quadrant
                case x__, y__ if x__<0 and y__<0:
                    match (x - x_origin, y - y_origin):
                        # first Quadrant
                        case x_, y_ if x_ > 0 and y_ > 0:
                            index = index
                        # second Quadrant
                        case x_, y_ if x_ < 0 and y_ > 0:
                            index = index+1
                        # third Quadrant
                        case x_, y_ if x_ < 0 and y_ < 0:
                            index = index+1
                        # fourth Quadrant
                        case x_, y_ if x_ > 0 and y_ < 0:
                            index = index
                        # origin
                        case x_, y_ if x_ == 0 and y_ == 0:
                            pass
                        # x axis positive
                        case x_, y_ if x_ > 0 and y_ == 0:
                            index = index
                        # x axis negative
                        case x_, y_ if x_ < 0 and y_ == 0:
                            index = index+1
                        # y axis positive
                        case x_, y_ if x_ == 0 and y_ > 0:
                            index = index
                        # y axis negative
                        case x_, y_ if x_ == 0 and y_ < 0:
                            index = index+1
                # fourth Quadrant
                case x__, y__ if x__>0 and y__<0:
                    match (x - x_origin, y - y_origin):
                        # first Quadrant
                        case x_, y_ if x_ > 0 and y_ > 0:
                            index = index
                        # second Quadrant
                        case x_, y_ if x_ < 0 and y_ > 0:
                            index = index
                        # third Quadrant
                        case x_, y_ if x_ < 0 and y_ < 0:
                            index = index+1
                        # fourth Quadrant
                        case x_, y_ if x_ > 0 and y_ < 0:
                            index = index+1
                        # origin
                        case x_, y_ if x_ == 0 and y_ == 0:
                            pass
                        # x axis positive
                        case x_, y_ if x_ > 0 and y_ == 0:
                            index = index
                        # x axis negative
                        case x_, y_ if x_ < 0 and y_ == 0:
                            index = index+1
                        # y axis positive
                        case x_, y_ if x_ == 0 and y_ > 0:
                            index = index
                        # y axis negative
                        case x_, y_ if x_ == 0 and y_ < 0:
                            index = index+1
                # origin
                case x__, y__ if x__==0 and y__==0:
                    pass
                # x axis positive
                case x_, y_ if x_>0 and y_==0:
                    index = index
                # x axis negative
                case x_, y_ if x_<0 and y_==0:
                    index = index+1
                # y axis positive
                case x_, y_ if x_==0 and y_>0:
                    index = index
                # y axis negative
                case x_, y_ if x_==0 and y_<0:
                    index = index+1

            polygon.points.insert(index, point)

        else:
            pos = dpg.get_plot_mouse_pos()
            points = [dpg.get_value(point)[:2] for point in polygon.points]

            index = closest_point_index(point=pos, points=points)
            nearest_point = polygon.points[index]
            dpg.delete_item(nearest_point)
            polygon.points.pop(index)

        self.update_polygon(polyname=polyname)

    def selected_polygon(self, _,app_data,userdata:str):
        if app_data:
            dpg.set_value("poly_selected", userdata)
            for row in dpg.get_item_children("tbl_polygons")[1]:
                if dpg.get_item_alias(row) == f"row_{userdata}":
                    continue

                dpg.set_value(dpg.get_item_children(row)[1][1], False)
        else:
            dpg.set_value("poly_selected", "")
