# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaGuiLib.controllers import ViewportController

from AthenaLib.models import Version

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Application:
    viewport:ViewportController

    version:Version
    restart:bool = False

    def version_to_str(self) -> str:
        """Returns the full version in string format"""
        return f"{self.version.major}.{self.version.minor}.{self.version.fix}"


    def __init__(self):
        # NEEDS TO BE FIRST!
        dpg.create_context()
        # Put all othert stuff below here in correct order
        self.viewport = ViewportController()

    def start(self):
        """
        Defines a loop, which in most cases will only run once, but allows for a restart of the application
        """
        while True:
            dpg.setup_dearpygui()
            dpg.show_viewport()
            dpg.start_dearpygui()  # blocking
            dpg.destroy_context()

            if self.restart:
                continue
            break
            # else, the restart option is set, and this will allow for a new application startup