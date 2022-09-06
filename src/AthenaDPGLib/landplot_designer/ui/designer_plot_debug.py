# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import contextlib
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.ui.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.landplot_designer.models.core import Core

from AthenaDPGLib.general.data.universal_tags import LandplotItems,LandplotSettings, LandplotDebug

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class DesignerPlotDebug(CustomDPGItem):
    size_scale:float = 1. # has to be a float for all numpy arrays to work correctly

    # tags used with dpg to assign items to
    #   defined as kwargs so the user can change these if for some reason a duplicate tag is created by the system
    #   by default they use tags imported from the UniversalTags enum
    window_tag:str = field(default=LandplotItems.debug_window)

    # - non init vars -

    # ------------------------------------------------------------------------------------------------------------------
    # - Init and Properties-
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # - DPG methods -
    # ------------------------------------------------------------------------------------------------------------------
    def add_dpg(self, **kwargs):
        with self.dpg(**kwargs):
            pass

    @contextlib.contextmanager
    def dpg(self, width:int=0, height:int=0) -> int|str:
        # body of what otherwise would be: self.__enter__
        with dpg.window(tag=self.window_tag,width=width,height=height, show=False) as window:
            with dpg.group():
                dpg.add_text("Custom Series: Drawing Options")
                dpg.add_checkbox(
                    label="Show Chunks",
                    source=LandplotSettings.plot_show_chunks,
                    callback=self.callback_show_chunks
                )
                dpg.add_checkbox(
                    label="Show Polygons",
                    source=LandplotSettings.plot_show_polygons,
                    callback=self.callback_show_polygons
                )
                dpg.add_checkbox(
                    label="Show Origins",
                    source=LandplotSettings.plot_show_origins,
                    callback=self.callback_show_origins
                )
            with dpg.group():
                dpg.add_text("Custom Series: Drawn Items")
                with dpg.group(horizontal=True):
                    dpg.add_text(source=LandplotDebug.shown_chunks)
                    dpg.add_text(source=LandplotDebug.shown_polygons)
                with dpg.group(horizontal=True):
                    dpg.add_text(source=LandplotDebug.plot_scale)
                    dpg.add_text(source=LandplotDebug.plot_offset)
                with dpg.group(horizontal=True):
                    dpg.add_text(source=LandplotDebug.plot_limit_min)
                    dpg.add_text(source=LandplotDebug.plot_limit_max)

            yield window # what __enter__ returns

        # body of what otherwise would be: self.__exit__
        #   Functions that depend on DPG items already existing
    @staticmethod
    def callback_show_chunks(_, app_data):
        Core.designer_plot.plot_show_chunks = app_data

    @staticmethod
    def callback_show_polygons(_, app_data):
        Core.designer_plot.plot_show_polygons = app_data

    @staticmethod
    def callback_show_origins(_, app_data):
        Core.designer_plot.plot_show_origins = app_data