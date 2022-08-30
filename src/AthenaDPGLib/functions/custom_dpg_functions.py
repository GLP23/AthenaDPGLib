# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from contextlib import contextmanager
from typing import Any, Callable
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@contextmanager
def grid_layout(columns:int, **kwargs):
    """
    Ease of use addition:
    Uses a table to create a mimic of a grid layout system
    """
    # remove the header row as in a layout this is never supposed to show up
    if "header_row" in kwargs:
        # todo check if this is the best course of action
        kwargs.pop("header_row")

    # Create the table and pre-create the amount of columns
    with dpg.table(header_row=False,**kwargs) as table:
        for _ in range(columns):
            dpg.add_table_column()

        # yield the table, so you can do the following:
        #   `with grid_layout(): ...`
        yield table