# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import contextlib
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.general.functions.mutex import run_in_mutex
from AthenaDPGLib.general.data.universal_tags import UniversalTags as ut

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class LandplotDesigner:

    # - non init vars -

    # tags used with dpg to assign items to
    #   defined as kwargs so the user can change these if for some reason a duplicate tag is created by the system
    #   by default they use tags imported from the UniversalTags enum
    window_tag:str = field(default=ut.landplot_window.value)
    plot_tag:str = field(default=ut.landplot_plot.value)
    axis_x_tag:str = field(default=ut.landplot_axis_x.value)
    axis_y_tag:str = field(default=ut.landplot_axis_y.value)

    def __init__(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG methods -
    # ------------------------------------------------------------------------------------------------------------------
    def add_dpg(self):
        """
        Equivalent of a dpg function that adds an item to the stack without being context managed
        It runs the context managed functions and doesn't return anything.
        """
        with self.dpg():
            pass

    @contextlib.contextmanager
    def dpg(self):
        """
        Equivalent of a dpg function that is context managed.
        Returns the tag of the window. This way it can be used to define more functions within it's `with` body.
        """
        # body of what otherwise would be: self.__enter__
        with dpg.window(tag=self.window_tag) as window:
            with dpg.plot(tag=self.plot_tag):
                dpg.add_plot_axis(axis=dpg.mvXAxis, tag=self.axis_x_tag)
                with dpg.plot_axis(axis=dpg.mvYAxis, tag=self.axis_y_tag):
                    dpg.add_custom_series(
                        x=[0,1],
                        y=[0,1],
                        channel_count=2,
                        callback=lambda s,a,u : self._custom_series_callback(s,a,u)
                    )

            yield window # what __enter__ returns

        # body of what otherwise would be: self.__exit__

    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Series Callback -
    # ------------------------------------------------------------------------------------------------------------------
    @run_in_mutex
    def _custom_series_callback(self, sender, app_data, user_data):
        print(sender)