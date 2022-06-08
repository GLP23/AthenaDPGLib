# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg
import sys
import ctypes
from pathlib import Path

# Custom Library
from AthenaColor import RGBA

# Custom Packages
from AthenaGuiLib.entities import Viewport
import AthenaGuiLib.res.strings as strings

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    eq=False,
    kw_only=True,
    slots=True
)
class ViewportController:
    _viewport : Viewport = field(init=False, default_factory=lambda : Viewport())

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def title(self) -> str:
        return self._viewport.title
    @title.setter
    def title(self, value:str):
        self._viewport.title = value
        dpg.set_viewport_title(self._viewport.title)

    def get_icon(self) -> str|Path:
        return self._viewport.icon_path

    def set_icon(self, icon_path:str|Path, ModelID:str):
        # Define application ICON,
        #   makes sure the APPLICATION icon is shown in the taskbar
        if sys.platform == "win32":  # WINDODWS NEEDS THIS to make this possible
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                ModelID
            )
        else:
            # TODO fix this! (aka, find out how to do this)
            raise NotImplementedError(strings.linux_notimplementederror)

        # actually set the icon
        self._viewport.icon_path = icon_path
        dpg.set_viewport_small_icon(self._viewport.icon_path)
        dpg.set_viewport_large_icon(self._viewport.icon_path)

    # width, height and pos are kept as dpg functions, as these can change quite drastically on calls for other settings
    @property
    def width(self) -> int:
        return dpg.get_viewport_width()
    @width.setter
    def width(self, value:int):
        dpg.set_viewport_width(value)
    @property
    def height(self) -> int:
        return dpg.get_viewport_height()
    @height.setter
    def height(self, value:int):
        dpg.set_viewport_height(value)
    @property
    def pos(self)->list[float]:
        return dpg.get_viewport_pos()
    @pos.setter
    def pos(self, value:list[float]):
        dpg.set_viewport_pos(value)

    @property
    def min_width(self) -> int:
        return self._viewport.min_width
    @min_width.setter
    def min_width(self, value:int):
        self._viewport.min_width = value
        dpg.set_viewport_min_width(self._viewport.min_width)

    @property
    def min_height(self) -> int:
        return self._viewport.min_height
    @min_height.setter
    def min_height(self, value:int):
        self._viewport.min_height = value
        dpg.set_viewport_min_height(self._viewport.min_height)

    @property
    def max_width(self) -> int:
        return self._viewport.max_width
    @max_width.setter
    def max_width(self, value:int):
        self._viewport.max_width=value
        dpg.set_viewport_max_width(self._viewport.max_width)

    @property
    def max_height(self) -> int:
        return self._viewport.max_height
    @max_height.setter
    def max_height(self, value:int):
        self._viewport.max_height = value
        dpg.set_viewport_max_height(self._viewport.max_height)

    @property
    def resizable(self) -> bool:
        return self._viewport.resizable
    @resizable.setter
    def resizable(self, value:bool):
        self._viewport.resizable = value
        dpg.set_viewport_resizable(self._viewport.resizable)

    @property
    def vsync(self):
        return self._viewport.vsync
    @vsync.setter
    def vsync(self, value:bool):
        self._viewport.vsync = value
        dpg.set_viewport_vsync(self._viewport.vsync)

    @property
    def always_on_top(self) -> bool:
        return self._viewport.always_on_top
    @always_on_top.setter
    def always_on_top(self, value:bool):
        self._viewport.always_on_top = value
        dpg.set_viewport_always_top(self._viewport.always_on_top)

    @property
    def decorated(self) -> bool:
        return self._viewport.decorated
    @decorated.setter
    def decorated(self, value:bool):
        self._viewport.decorated=value
        dpg.set_viewport_decorated(self._viewport.decorated)

    @property
    def background_color(self):
        return self._viewport.background_color
    @background_color.setter
    def background_color(self, value:RGBA):
        self._viewport.background_color = value
        # noinspection PyTypeChecker
        dpg.set_viewport_clear_color(self._viewport.background_color.export())


