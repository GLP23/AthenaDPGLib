# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import contextlib
from abc import ABC, abstractmethod

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomDPGItem(ABC):
    window_tag: str

    @abstractmethod
    def add_dpg(self, **kwargs):
        """
        Equivalent of a dpg function that adds an item to the stack without being context managed
        It runs the context Any functions and doesn't return anything.
        """

    @abstractmethod
    def dpg(self, **kwargs) -> int | str:
        """
        Equivalent of a dpg function that is context managed.
        Returns the tag of the window. This way it can be used to define more functions within it's `with` body.
        """