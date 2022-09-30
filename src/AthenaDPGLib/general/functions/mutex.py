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
    """
    Decorator that runs the function iun a locked dpg.mutex state.
    Unlocks the mutex after the function has been run.
    """
    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        with dpg.mutex():
            return fnc(*args, **kwargs)
    return wrapper
