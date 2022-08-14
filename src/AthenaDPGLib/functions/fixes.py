# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import sys
import ctypes
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def fix_icon_for_taskbar(app_model_id:str):
    # Define application ICON,
    #   makes sure the APPLICATION icon is shown in the taskbar
    #   make sure that dpg.viewport(large_icon=..., small_icon=...) kwargs are both set
    if (sys_platform := sys.platform) == "win32":
        # WINDOWS NEEDS THIS to make this possible
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_model_id)
    else:
        # TODO fix this! (aka, find out how to do this)
        raise NotImplementedError(f"the 'fix_icon_for_taskbar' function doe not work for the os: {sys_platform}")

def fix_grid_layout_equal_row_spacing(table_name:str):
    if dpg.does_item_exist(table_name):
        child = dpg.get_item_children(table_name)
        vp_height = dpg.get_item_height(table_name)
        for x in child[1]:
            dpg.configure_item(x, height=vp_height / len(child[1]))