# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import itertools

import dearpygui.dearpygui as dpg
import contextlib
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import ArrayLike

# Custom Library
from AthenaLib.constants.types import COLOR
from AthenaColor.data.colors_html import DARKRED, ROYALBLUE

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
from AthenaDPGLib.landplot_designer.models.chunk import Chunk
from AthenaDPGLib.landplot_designer.functions.polygon_constructors import test_polygons
import AthenaDPGLib.landplot_designer.data.memory as Memory


from AthenaDPGLib.general.functions.mutex import run_in_mutex_method
from AthenaDPGLib.general.data.universal_tags import UniversalTags as ut

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
color_fill: COLOR = ROYALBLUE
color_border: COLOR = ROYALBLUE
color_origin: COLOR = DARKRED

@dataclass(slots=True, kw_only=True)
class LandplotDesigner:
    size_scale:float = 1.

    # tags used with dpg to assign items to
    #   defined as kwargs so the user can change these if for some reason a duplicate tag is created by the system
    #   by default they use tags imported from the UniversalTags enum
    window_tag:str = field(default=ut.landplot_window.value)
    plot_tag:str = field(default=ut.landplot_plot.value)
    axis_x_tag:str = field(default=ut.landplot_axis_x.value)
    axis_y_tag:str = field(default=ut.landplot_axis_y.value)

    # - non init vars -
    plot_axis_limit:int = field(init=False, default=10) # Positive direction. Governs how "precise" the plot is

    # ------------------------------------------------------------------------------------------------------------------
    # - Support methods for item scaling-
    # ------------------------------------------------------------------------------------------------------------------
    def _s(self, value:int) -> int:
        """
        Function which has to be used for any and all scaling in pixelspace,
            so the items are correctly scaled for non 1080p screens.
        """
        return round(value * self.size_scale)

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG methods -
    # ------------------------------------------------------------------------------------------------------------------
    def add_dpg(self, **kwargs):
        """
        Equivalent of a dpg function that adds an item to the stack without being context managed
        It runs the context managed functions and doesn't return anything.
        """
        with self.dpg(**kwargs):
            pass

    @contextlib.contextmanager
    def dpg(self, width:int=1000, height:int=1000) -> int|str:
        """
        Equivalent of a dpg function that is context managed.
        Returns the tag of the window. This way it can be used to define more functions within it's `with` body.
        """
        # body of what otherwise would be: self.__enter__
        with dpg.window(tag=self.window_tag,width=width,height=height) as window:
            # ----------------------------------------------------------------------------------------------------------
            # Create the plot and all it's systems
            with dpg.plot(tag=self.plot_tag, width=self._s(750), height=self._s(750)):
                with self._constructor_plot_axis(axis=dpg.mvXAxis, tag=self.axis_x_tag): pass
                with self._constructor_plot_axis(axis=dpg.mvYAxis, tag=self.axis_y_tag):
                    dpg.add_custom_series(
                        x=[0,1],
                        y=[0,1],
                        channel_count=2,
                        # callback=self._custom_series_callback
                        callback=self._custom_series_callback
                    )

            # ----------------------------------------------------------------------------------------------------------
            yield window # what __enter__ returns

        # body of what otherwise would be: self.__exit__

    @contextlib.contextmanager
    def _constructor_plot_axis(self, axis:int, tag:str) -> int|str:
        """
        Simple constructor for plot axis
        """
        with dpg.plot_axis(
            axis=axis,
            tag=tag,
            # no_gridlines=True,
            # no_tick_marks=True,
            # no_tick_labels=True
        ) as plot:
            yield plot

        # set the limits of the plot
        #   this is due to the fact that the plot will not be used as a plot
        #   but as the "center of the camera axis"
        # dpg.set_axis_limits(tag, ymin=-self.plot_axis_limit, ymax=self.plot_axis_limit)
        # dpg.set_axis_limits(tag, ymin=-5000, ymax=5000)



    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Series Callback -
    # ------------------------------------------------------------------------------------------------------------------
    @run_in_mutex_method
    def _custom_series_callback(self, sender, app_data, user_data):
        global color_border, color_fill, color_fill

        # todo
        #   check if this can be created once and then just stored
        pos_0_0 = np.array([app_data[1][0],app_data[2][0]])
        pos_difference = np.array([app_data[1][1],app_data[2][1]])-pos_0_0

        # delete old drawn items
        #   else we won't update, but simply append to the old image
        #   adding new layers on top of the drawn pieces
        dpg.delete_item(sender, children_only=True, slot=2)
        dpg.push_container_stack(sender)

        # DO STUFF
        # --------------------------------------------------------------------------------------------------------------
        for chunk in Memory.chunk_manager.chunks(): #type: Polygon
            dpg.draw_polygon(
                points=[
                    (point*pos_difference)+pos_0_0
                    for point in chunk.points_absolute #type: ArrayLike
                ],
                fill=(0,255,0,32),
                color=(0,255,0,32),
                thickness=0
            )

        for poly in  (
                landplot
                for chunk in Memory.chunk_manager.chunks() #type: Chunk
                for landplot in chunk.land_plots
            ):
            # print(poly)
            dpg.draw_polygon(
                points=[
                    (point*pos_difference)+pos_0_0
                    for point in poly.points_absolute #type: ArrayLike
                ],
                fill=color_fill,
                color=color_border,
                thickness=0
            )

            dpg.draw_circle(
                center=(poly.origin*pos_difference)+pos_0_0,
                radius=5,
                fill=color_origin,
                color=color_origin,
                thickness=0
            )

        # --------------------------------------------------------------------------------------------------------------
        # After everything has been drawn
        dpg.pop_container_stack()