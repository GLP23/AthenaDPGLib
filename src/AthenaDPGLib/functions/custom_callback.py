# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.models.custom_callbacks import CustomCallbacks

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def apply_callbacks():
    """
    Goes over all registered callbacks and sets the items' callbacks accordingly
    Will raise errors if the tag doesn't exist yet.
    This system works because CustomCallbacks only has ClassVar and ClassMethods
    """
    for tag in CustomCallbacks.mapping_callback:
        if dpg.does_item_exist(item=tag):
            dpg.set_item_callback(item=tag, callback=CustomCallbacks.chain_callback)
    for tag in CustomCallbacks.mapping_drag_callback:
        if dpg.does_item_exist(item=tag):
            dpg.set_item_callback(item=tag, callback=CustomCallbacks.chain_drag_callback)
    for tag in CustomCallbacks.mapping_drop_callback:
        if dpg.does_item_exist(item=tag):
            dpg.set_item_callback(item=tag, callback=CustomCallbacks.chain_drop_callback)

    dpg.set_viewport_resize_callback(callback=CustomCallbacks.chain_viewport_resize)

def apply_callbacks_specific(items:set[str]):
    """
    Goes over all items and sets those item's callbacks if the dpg items exist
    This system works because CustomCallbacks only has ClassVar and ClassMethods
    """
    for tag in items:
        if dpg.does_item_exist(item=tag):
            if tag in CustomCallbacks.mapping_callback:
                dpg.set_item_callback(item=tag, callback=CustomCallbacks.chain_callback)

            if tag in CustomCallbacks.mapping_drag_callback:
                dpg.set_item_callback(item=tag, callback=CustomCallbacks.chain_drag_callback)

            if tag in CustomCallbacks.mapping_drop_callback:
                dpg.set_item_callback(item=tag, callback=CustomCallbacks.mapping_drop_callback)