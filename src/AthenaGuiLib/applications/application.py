# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
import ctypes
import sys
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.models import Version

# Custom Packages
from AthenaGuiLib.viewports import Viewport

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    slots=True,
    kw_only=True
)
class Application: # made a singleton to make sure that there is only one application per run
    """
    A DearPyGui application.
    Because DPG is a functional based wrapper, there is no inheritance from any DPG application class, as this doesn't exist.
    This class is meant to store various information about the application and run certain events in certain manners.
    """

    title:str="UNDEFINED"   # application title, shown at the top of the window, and is the name you find in the taskbar
    version:Version=field(default_factory=lambda:Version(0,"PreAlpha",0))
    icon_enabled:bool=True
    viewports:set[Viewport,...]=field(default_factory=set)

    # paths to files
    icon_path:str=None
    settings_path:str=None

    # ------------------------------------------------------------------------------------------------------------------
    # - Init stuff-
    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        # create the context to make sure we can make viewports, windows etc
        dpg.create_context() # doesn't return a value, so can just be dne here, without setting the resul to a slot

    # ------------------------------------------------------------------------------------------------------------------
    # - Settings stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def get_settings_from_file(self):
        # check if te filepath has been defined or not
        if self.settings_path is None or not os.path.isfile(self.settings_path):
            raise FileNotFoundError("No settings file could be found")

        with open(self.settings_path, "r") as file:
            settings_dict = json.load(file)
        return settings_dict

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def model_id(self):
        return f"{self.title}[{self.version.to_str(sep='.')}]"

    # ------------------------------------------------------------------------------------------------------------------
    # - Viewport stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def get_viewport(self) -> Viewport:
        # if no viewport has been defined yet, you need to make one
        #   Else dpg will fail
        if not self.viewports:
            viewport = Viewport()
            self.viewports.add(viewport)
        else:
            # currently in dpg there is only one viewport available, but this will change in later versions
            viewport, = self.viewports
        return viewport

    # ------------------------------------------------------------------------------------------------------------------
    # - Fixes -
    # ------------------------------------------------------------------------------------------------------------------
    def fix_icon_for_taskbar(self):
        # retrieve the viewport object, if it hasn't been done before, it'll set up a new one
        viewport:Viewport = self.get_viewport()

        # Define application ICON,
        #   makes sure the APPLICATION icon is shown in the taskbar
        if sys.platform == "win32":
            # WINDOWS NEEDS THIS to make this possible
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                self.model_id
            )
        else:
            # TODO fix this! (aka, find out how to do this)
            raise NotImplementedError

        # actually set the icon
        if self.icon_enabled:
            viewport.set_icon(icon_path=self.icon_path)

    # ------------------------------------------------------------------------------------------------------------------
    # - Startup and Close down -
    # ------------------------------------------------------------------------------------------------------------------
    def graceful_minimum_shutdown(self):
        """the bare minimum that needs to happen to make sure the shutdown is handled correctly"""
        # destroy the context, else dpg will freak out
        dpg.destroy_context()

    def launch(self):
        try:
            dpg.setup_dearpygui()
            dpg.show_viewport()
            # launching of the actual application
            dpg.start_dearpygui() # blocking call
        except KeyboardInterrupt: # made sure to do a "graceful" shutdown:
            self.graceful_minimum_shutdown()
            raise
        else:
            self.graceful_minimum_shutdown() # always make sure there is some form of 'graceful' shutdown
        # everything after is done after dpg has been shut down
        #   should handle things like dumping the settings to file
        #   etc...