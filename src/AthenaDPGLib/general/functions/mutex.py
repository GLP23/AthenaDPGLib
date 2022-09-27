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
    def wrapper(*args, **kwargs):
        with dpg.mutex():
            return fnc(*args, **kwargs)
    return wrapper

def run_in_mutex__as_callback(fnc):
    @functools.wraps(fnc)
    def wrapper(sender, app_data, user_data):
        with dpg.mutex():
            return fnc(sender, app_data, user_data)
    return wrapper

def run_in_mutex_method__as_callback(fnc):
    @functools.wraps(fnc)
    def wrapper(obj, sender, app_data, user_data):
        with dpg.mutex():
            return fnc(obj, sender, app_data, user_data)
    return wrapper

