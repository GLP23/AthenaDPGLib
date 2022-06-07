# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field
import sys
import ctypes

# Custom Library
from AthenaGuiLib.models import (AppInfo, AppSettings)
import AthenaGuiLib.res.strings as strings

from AthenaColor import RGB, RGBA

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Application:
    """
    Class to house all logic and data behind an application

    Order of calls:
        .viewport_define()

        .launch()

    """
    # Keyword arguments on init
    info: AppInfo = field(default_factory=AppInfo.factory)  # All info data is frozen across the instance of an application
    settings: AppSettings = field(default_factory=AppSettings.factory) # All settings can be changed while the application is running

    # class attributes not to be setup on init
    _viewport_setup:bool = field(init=False, default=False)

    # ------------------------------------------------------------------------------------------------------------------
    # - Propeties -
    # ------------------------------------------------------------------------------------------------------------------


    # ------------------------------------------------------------------------------------------------------------------
    # - Viewport related settings -
    # ------------------------------------------------------------------------------------------------------------------
    def viewport_define(self):
        dpg.create_viewport(
            title=self.info.name,
            #icons are set up in the method self._viewport_icon()
            # small_icon=...,
            # large_icon=...,

            width=self.settings.width,
            height=self.settings.height,
            x_pos=self.settings.x_pos,
            y_pos=self.settings.y_pos,
            min_width=self.info.min_width,
            max_width=self.info.max_width,
            min_height=self.info.min_height,
            max_height=self.info.max_height,
            resizable=self.info.resizable,
            # vsync=None,
            always_on_top=self.info.always_on_top,
            decorated=self.info.decorated,
            # Clear color is handled by self.set_background_color()
            # clear_color=...,
        )

        # Define the icon for the viewport
        self._viewport_icon()

        # Define the background color
        self.set_background_color(self.info.clear_color)

        # once everything has been set up, set the boolean to true, else the .launch() will fail
        self._viewport_setup = True

        # return self to chain methods after eachother
        return self

    def _viewport_icon(self):
        # in the info class this can be defined
        if self.info.icon_to_taskbar:
            # Define application ICON,
            #   makes sure the APPLICATION icon is shown in the taskbar
            if sys.platform == "win32":  # WINDODWS NEEDS THIS to make this possible
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    f"{self.info.name}[{self.info.version_to_str()}]"
                )
            elif sys.platform in ("linux", "linux2"):
                # TODO fix this! (aka, find out how to do this)
                raise NotImplementedError(strings.linux_notimplementederror)

    # ------------------------------------------------------------------------------------------------------------------
    # - Application function - TODO change this to another object
    # ------------------------------------------------------------------------------------------------------------------
    def set_background_color(self, color:RGB|RGBA):
        dpg.set_viewport_clear_color(color.export())

    # ------------------------------------------------------------------------------------------------------------------
    # - Launch and quit of the program-
    # ------------------------------------------------------------------------------------------------------------------
    def quit(self):
        dpg.destroy_context()

    def launch(self) -> None:
        # set up the basicis of the dpg
        dpg.create_context()

        self.viewport_define()

        dpg.setup_dearpygui()

        dpg.attr

        dpg.show_viewport()

        dpg.start_dearpygui() # blocking

        self.quit()

        # Returns None because the following functions of dpg
        #   ( dpg.start_dearpygui() dpg.destroy_context() ) don't return any values,
        #   and can therefor not return any exit codes
        return

