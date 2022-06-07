# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass
import ctypes
import sys

# Custom Library
from AthenaGuiLib.application.application import Application

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Viewport:
    @staticmethod
    def __post_init__():
        dpg.create_viewport()

    @staticmethod
    def set_icon(app:Application):
        # Define application ICON,
        #   makes sure the application icon is shown in the taskbar
        if sys.platform == "win32":  # WINDODWS NEEDS THIS to make this possible
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"{app.info.name}[{app.info.version}]")
        elif sys.platform in ("linux", "linux2"):
            raise NotImplementedError  # TODO fix this!

        dpg.set_viewport_small_icon(app.info.icon)
        dpg.set_viewport_large_icon(app.info.icon)

    @staticmethod
    def show():
        dpg.show_viewport()

    @staticmethod
    def set_title(app:Application):
        dpg.set_viewport_title(app.info.name)

    @staticmethod
    def toggle_fullscreen():
        dpg.toggle_viewport_fullscreen()