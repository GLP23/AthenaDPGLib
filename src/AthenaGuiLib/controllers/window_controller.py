# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaGuiLib.entities import Window

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class WindowController:
    _window:Window

    def __init__(self, label:str="window"):
        self._window = Window(
            id = dpg.add_window(
                label=label
            )
        )

    @property
    def id(self):
        return self._window.id

    def content(self):
        pass

    def assemble(self):