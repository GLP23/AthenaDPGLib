# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import contextlib

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class LandplotDesigner:
    window_tag:int|str
    def __init__(self):
        pass

    def add_dpg(self):
        """
        Equivalent of a dpg function that adds an item to the stack without being context managed
        It runs the context managed functions and doesn't return anything.
        """
        with self.dpg():
            pass

    @contextlib.contextmanager
    def dpg(self):
        """
        Equivalent of a dpg function that is context managed.
        Returns the tag of the window. This way it can be used to define more functions within it's `with` body.
        """
        # __enter__
        with dpg.window() as window:
            # store the tag for future reference
            self.window_tag = window

            yield window # what __enter__ returns

        # __exit__