# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import contextlib
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import ArrayLike
from typing import Callable

# Custom Library
from AthenaLib.constants.types import COLOR
from AthenaColor.data.colors_html import DARKRED, ROYALBLUE

# Custom Packages
from AthenaDPGLib.landplot_designer.ui.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.landplot_designer.models.chunk import Chunk
from AthenaDPGLib.landplot_designer.models.core import Core
from AthenaDPGLib.landplot_designer.functions.decorators import update_renderable_chunks

from AthenaDPGLib.general.functions.mutex import run_in_mutex_method__as_callback, run_in_mutex
from AthenaDPGLib.general.data.universal_tags import LandplotItems, LandplotSettings, LandplotDebug

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
color_fill: COLOR = ROYALBLUE
color_border: COLOR = color_fill
color_origin: COLOR = DARKRED

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class DesignerPlot(CustomDPGItem):
    size_scale:float = 1. # has to be a float for all numpy arrays to work correctly

    # tags used with dpg to assign items to
    #   defined as kwargs so the user can change these if for some reason a duplicate tag is created by the system
    #   by default they use tags imported from the UniversalTags enum
    window_tag:str = field(default=LandplotItems.window)
    plot_tag:str = field(default=LandplotItems.plot)
    plot_registry_tag:str = field(default=LandplotItems.plot_registry)
    axis_x_tag:str = field(default=LandplotItems.axis_x)
    axis_y_tag:str = field(default=LandplotItems.axis_y)

    # - non init vars -
    plot_axis_limit:float = field(init=False, default=100.) # Positive direction. Governs how "precise" the plot is
    _mouse_plot_pos_old:ArrayLike = field(init=False, default_factory=lambda :np.array((0., 0.)))
    _plot_offset:ArrayLike = field(init=False, default_factory=lambda :np.array((0., 0.)))
    _plot_scale:float = field(init=False, default=1.)
    _plot_scale_step:float = field(init=False, default=0.025)
    _plot_limit_min:ArrayLike = field(init=False)
    _plot_limit_max:ArrayLike = field(init=False)
    _plot_registry_callback:dict[int:Callable] = field(init=False)

    # ------------------------------------------------------------------------------------------------------------------
    # - Init and Properties-
    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        # Vars that depend on vars that are defined on init
        self._plot_limit_min = np.array([-self.plot_axis_limit, -self.plot_axis_limit])
        self._plot_limit_max = np.array([self.plot_axis_limit, self.plot_axis_limit])
        self._plot_registry_callback = {
            dpg.mvKey_Add : self._plot_update_onvisible__key_down_add,
            dpg.mvKey_Subtract : self._plot_update_onvisible__key_down_subtract
        }

    # Properties that are just getters of internal values
    #   Most likely used for cross component functions
    @property
    def plot_limit_min(self):
        return self._plot_limit_min
    @property
    def plot_limit_max(self):
        return self._plot_limit_max
    @property
    def plot_scale(self):
        return self._plot_scale
    @property
    def plot_offset(self):
        return self._plot_offset

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
        with self.dpg(**kwargs):
            pass

    @update_renderable_chunks
    @contextlib.contextmanager
    def dpg(self, width:int=1000, height:int=1000) -> int|str:
        # body of what otherwise would be: self.__enter__
        with dpg.window(tag=self.window_tag,width=width,height=height) as window:
            with dpg.group(horizontal=True):
                # ------------------------------------------------------------------------------------------------------
                # Create the plot and all it's systems
                with dpg.plot(tag=self.plot_tag, width=self._s(750), height=self._s(750)):
                    with self._constructor_plot_axis(axis=dpg.mvXAxis, tag=self.axis_x_tag): pass
                    with self._constructor_plot_axis(axis=dpg.mvYAxis, tag=self.axis_y_tag):
                        dpg.add_custom_series(
                            x=[0,1],
                            y=[0,1],
                            channel_count=2,
                            callback=self._custom_series_callback
                        )

                dpg.add_button(label="Show Debug", callback=self._show_debug_callback)

            yield window # what __enter__ returns

        # body of what otherwise would be: self.__exit__
        #   Functions that depend on DPG items already existing
        self.registry_system()

    def _show_debug_callback(self):
        if not dpg.is_item_shown(LandplotItems.debug_window):
            dpg.show_item(LandplotItems.debug_window)

    @contextlib.contextmanager
    def _constructor_plot_axis(self, axis:int, tag:str) -> int|str:
        """
        Simple constructor for plot axis
        """
        with dpg.plot_axis(
            axis=axis,
            tag=tag,
            no_gridlines=True,
            no_tick_marks=True,
            no_tick_labels=True
        ) as plot:
            yield plot

        # set the limits of the plot
        #   this is due to the fact that the plot will not be used as a plot
        #   but as the "center of the camera axis"
        dpg.set_axis_limits(tag, ymin=-self.plot_axis_limit, ymax=self.plot_axis_limit)

    def registry_system(self):
        # Registry : PLOT
        with dpg.item_handler_registry(tag=self.plot_registry_tag):
            dpg.add_item_visible_handler(callback=self._plot_update_onvisible)
            dpg.add_item_clicked_handler(callback=self._plot_update_onclick)

        dpg.bind_item_handler_registry(
            handler_registry=self.plot_registry_tag,
            item=self.plot_tag
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Plot Offset system -
    # ------------------------------------------------------------------------------------------------------------------
    def _plot_update_onvisible(self):
        """
        Function which combines all callbacks for the "plot_on_visible" section of the registry
        """
        if dpg.is_item_hovered(self.plot_tag):
            if dpg.is_mouse_button_dragging(dpg.mvMouseButton_Left, threshold=0.1):
                self._plot_update_onvisible__dragging()

            for key, callback in self._plot_registry_callback.items():
                if dpg.is_key_pressed(key=key) or dpg.is_key_down(key=key):
                    callback()

    @update_renderable_chunks
    @run_in_mutex
    def _plot_update_onvisible__dragging(self):
        """
        When dragging on the plot
        """
        pos_plot_space = np.array(dpg.get_plot_mouse_pos())

        # noinspection PyUnresolvedReferences
        if self._mouse_plot_pos_old.all() != np.array((0., 0.)).all():
            self._plot_offset -= (self._mouse_plot_pos_old - pos_plot_space) * (1 / self._plot_scale)

        self._mouse_plot_pos_old = pos_plot_space

    @update_renderable_chunks
    @run_in_mutex
    def _plot_update_onvisible__key_down_add(self):
        """
        When the addition key is held down on the plot
        """
        self._plot_scale += self._plot_scale_step

    @update_renderable_chunks
    @run_in_mutex
    def _plot_update_onvisible__key_down_subtract(self):
        """
        When the subtraction key is held down on the plot
        """
        if self._plot_scale <= self._plot_scale_step:
            self._plot_scale = self._plot_scale_step
        else:
            self._plot_scale -= self._plot_scale_step

    @update_renderable_chunks
    @run_in_mutex
    def _plot_update_onclick(self):
        self._mouse_plot_pos_old = np.array([0.,0.])

    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Series Callback -
    # ------------------------------------------------------------------------------------------------------------------
    @run_in_mutex_method__as_callback
    def _custom_series_callback(self, sender, app_data, _):
        global color_border, color_fill, color_fill

        # todo
        #   check if this can be created once and then just stored
        pos_0_0 = np.array([app_data[1][0],app_data[2][0]])
        pos_1_1 = np.array([app_data[1][1],app_data[2][1]])
        pos_difference = (pos_1_1-pos_0_0) * self._plot_scale
        i=0

        show_chunks = dpg.get_value(LandplotSettings.plot_show_chunks)
        show_polygons = dpg.get_value(LandplotSettings.plot_show_polygons)
        show_origins = dpg.get_value(LandplotSettings.plot_show_origins)

        # delete old drawn items
        #   else we won't update, but simply append to the old image
        #   adding new layers on top of the drawn pieces
        dpg.delete_item(sender, children_only=True, slot=2)
        dpg.push_container_stack(sender)

        # DO STUFF
        # --------------------------------------------------------------------------------------------------------------
        if show_chunks:
            for i, chunk in enumerate(Core.chunk_manager.get_renderable_chunks(), start=1): #type: int, Chunk
                dpg.draw_polygon(
                    points=[
                        (((point+self._plot_offset)*pos_difference)+pos_0_0)
                        for point in chunk.points_absolute #type: ArrayLike
                    ],
                    fill=(0,255,0,32),
                    color=(0,255,0,32),
                    thickness=0
                )

        if show_polygons or show_origins:
            for i, chunk in enumerate(Core.chunk_manager.get_renderable_chunks(), start=1):  # type: int, Chunk
                for land_plot in chunk.land_plots:
                    if show_polygons:
                        dpg.draw_polygon(
                            points=[
                                (((point+self._plot_offset)*pos_difference)+pos_0_0)
                                for point in land_plot.points_absolute #type: ArrayLike
                            ],
                            fill=color_fill,
                            color=color_border,
                            thickness=0
                        )
                    if show_origins:
                        dpg.draw_circle(
                            center=(((land_plot.origin + self._plot_offset) * pos_difference) + pos_0_0),
                            radius=5,
                            fill=color_origin,
                            color=color_origin,
                            thickness=0
                        )

        # --------------------------------------------------------------------------------------------------------------
        # After everything has been drawn
        dpg.pop_container_stack()
        dpg.set_value(LandplotDebug.shown_polygons, f"poly: {len(dpg.get_item_children(sender,2))}")
        dpg.set_value(LandplotDebug.shown_chunks, f"chunks: {i}")