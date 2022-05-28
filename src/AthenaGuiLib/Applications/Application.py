# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import ctypes

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Application:
    _icon:str

    def __init__(self, name:str, version:tuple):
        # makes sure the application icon is shown in the taskbar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID()

    @property
    def icon(self):
        return self._icon_small, self._icon_large

    @icon.setter
    def icon(self, path):
        self._icon_small = dpg.set_viewport_small_icon(path)
        self._icon_large = dpg.set_viewport_large_icon(path)