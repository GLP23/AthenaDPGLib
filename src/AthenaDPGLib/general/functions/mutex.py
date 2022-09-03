# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import functools
import dearpygui.dearpygui as dpg


# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def run_in_mutex(fnc):
    @functools.wraps(fnc)
    def wrapper(sender, app_data, user_data):
        with dpg.mutex():
            return fnc(sender, app_data, user_data)
    return wrapper
