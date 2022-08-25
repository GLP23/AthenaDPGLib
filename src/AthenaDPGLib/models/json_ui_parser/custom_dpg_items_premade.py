# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from contextlib import contextmanager

# Custom Library

# Custom Packages
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
    # TODO check how to decouple from CustomDPGItems
    #   so it has it's own class var `items` and `items_context_managed`

    # ------------------------------------------------------------------------------------------------------------------
    # - Custom Objects -
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    @CustomDPGItems.custom_dpg_item_context_managed
    @contextmanager
    def primary_window(attrib:dict):
        """
        Easy way to assign a primary window
        Make sure the `tag` kwarg is defined in the item's attributes
        """
        with dpg.window(**attrib) as window:
            # child items handled here after the yield
            yield window

        # After all has been created
        #   set the primary window. Can't do this before the actual window exists
        dpg.set_primary_window(attrib["tag"], True)
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    @CustomDPGItems.custom_dpg_item
    def viewport(attrib:dict):
        """
        Overwrites the "normal" dpg function which is used by the parser
        Meant to immediately fix the icon for the taskbar if needed
        """
        dpg.create_viewport(**attrib)
        if any(i in attrib for i in ["large_icon", "small_icon"]):
            fix_icon_for_taskbar("AthenaApplication")

    # ------------------------------------------------------------------------------------------------------------------
