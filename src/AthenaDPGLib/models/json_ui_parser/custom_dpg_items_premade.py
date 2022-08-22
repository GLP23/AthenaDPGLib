# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from contextlib import contextmanager

# Custom Library

# Custom Packages
from AthenaDPGLib.data.exceptions import error_tag
from AthenaDPGLib.functions.fixes import fix_icon_for_taskbar
from AthenaDPGLib.models.json_ui_parser.custom_dpg_items import CustomDPGItems

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomDPGItems_PreMade(CustomDPGItems):
    """
    A collection of already PreMade custom items
    These items are frequently used or fix issues that otherwise cost more coding time to fix for every application
        (see viewport)
    """
    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Objects -
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    @CustomDPGItems.custom_dpg_item_context_managed
    @contextmanager
    def primary_window(*,item:str, attrib:dict, tags:set):
        """
        Easy way to assign a primary window
        """
        # store the tag else the tag can technically be reused,
        #   which is not something we want, else DPG is going to flip
        if (tag:="primary_window") in tags:
            raise error_tag(tag, item)

        with dpg.window(tag=tag, **attrib) as window:
            # child items handled here after the yield
            yield window

        # After all has been created
        #   set the primary window. Can't do this before the actual window exists
        dpg.set_primary_window(tag, True)
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    @CustomDPGItems.custom_dpg_item
    def viewport(*,attrib:dict, **_):
        """
        Overwrites the "normal" dpg function which is used by the parser
        Meant to immediately fix the icon for the taskbar if needed
        """
        dpg.create_viewport(**attrib)
        if "large_icon" in attrib or "small_icon" in attrib:
            fix_icon_for_taskbar("AthenaApplication")

    # ------------------------------------------------------------------------------------------------------------------
