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
from AthenaDPGLib.landplot_designer.ui._custom_dpg_item import CustomDPGItem
import AthenaDPGLib.landplot_designer.data.memory as Memory

import AthenaDPGLib.general.data.universal_tags as ut

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class LandplotDesignerDebug(CustomDPGItem):
    size_scale:float = 1. # has to be a float for all numpy arrays to work correctly

    # tags used with dpg to assign items to
    #   defined as kwargs so the user can change these if for some reason a duplicate tag is created by the system
    #   by default they use tags imported from the UniversalTags enum
    window_tag:str = field(default=ut.landplot_debug_window)

    # - non init vars -

    # ------------------------------------------------------------------------------------------------------------------
    # - Init and Properties-
    # ------------------------------------------------------------------------------------------------------------------

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
    def dpg(self, width:int=0, height:int=0) -> int|str:
        """
        Equivalent of a dpg function that is context managed.
        Returns the tag of the window. This way it can be used to define more functions within it's `with` body.
        """
        # body of what otherwise would be: self.__enter__
        with dpg.window(tag=self.window_tag,width=width,height=height, show=False) as window:
            with dpg.group():
                dpg.add_text("Custom Series: Drawing Options")
                dpg.add_checkbox(
                    label="Show Chunks",
                    default_value=Memory.landplot_designer.plot_show_chunks,
                    callback=self.callback_show_chunks
                )
                dpg.add_checkbox(
                    label="Show Polygons",
                    default_value=Memory.landplot_designer.plot_show_polygons,
                    callback=self.callback_show_polygons
                )
                dpg.add_checkbox(
                    label="Show Origins",
                    default_value=Memory.landplot_designer.plot_show_origins,
                    callback=self.callback_show_origins
                )
            with dpg.group():
                dpg.add_text("Custom Series: Drawn Items")
                dpg.add_text(tag="chunks")
                dpg.add_text(tag="polygons")
                dpg.add_text(tag="offset")
                dpg.add_text(tag="scale")

            yield window # what __enter__ returns

        # body of what otherwise would be: self.__exit__
        #   Functions that depend on DPG items already existing
    @staticmethod
    def callback_show_chunks(_, app_data):
        Memory.landplot_designer.plot_show_chunks = app_data

    @staticmethod
    def callback_show_polygons(_, app_data):
        Memory.landplot_designer.plot_show_polygons = app_data

    @staticmethod
    def callback_show_origins(_, app_data):
        Memory.landplot_designer.plot_show_origins = app_data