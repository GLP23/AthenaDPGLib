# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import asyncio
import json
import os
from dataclasses import dataclass, field
import ctypes
import sys
import dearpygui.dearpygui as dpg
from typing import Callable

# Custom Library
from AthenaLib.models import Version

# Custom Packages
from AthenaGuiLib.models.viewports import Viewport
from AthenaGuiLib.models.settings import Settings

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

    # asyncio stuff
    loop:asyncio.AbstractEventLoop = field(default_factory=asyncio.new_event_loop)

    # --- special classes ---
    # Settings
    settings_class:type = Settings
    settings:Settings = field(init=False)
    _settings_defined:bool = field(init=False, default=False)
    post_dpg_launchers:list[Callable] = field(init=False, default_factory=list)
    process_custom_settings:Callable = None

    # ------------------------------------------------------------------------------------------------------------------
    # - Init stuff-
    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        # create the context to make sure we can make viewports, windows etc
        dpg.create_context() # doesn't return a value, so can just be dne here, without setting the resul to a slot

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def model_id(self):
        return f"{self.title}[{self.version.to_str(sep='.')}]"

    # ------------------------------------------------------------------------------------------------------------------
    # - Settings stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def settings_retrieve_from_file(self) -> Application:
        # check if te filepath has been defined or not
        if self.settings_path is None or not os.path.isfile(self.settings_path):
            raise FileNotFoundError("No settings file could be found")

        with open(self.settings_path, "r") as file:
            self.settings = self.settings_class(json.load(file))

        # Process settings at the beginning of the application
        if self.settings.values.fullscreen:
            dpg.toggle_viewport_fullscreen()
        if self.settings.values.maximized:
            self.post_dpg_launchers.append(dpg.maximize_viewport)

        # process the custom defined settings
        #   This is done by defining a function to handle this
        if self.process_custom_settings is not None:
            self.process_custom_settings()

        # return itself to make these functions chainable
        return self

    def settings_store(self) -> Application:
        with open(self.settings_path, "w") as settings_file:
            settings_file.write(json.dumps(self.settings.to_dict()))
        # return itself to make these functions chainable
        return self

    # ------------------------------------------------------------------------------------------------------------------
    # - Viewport stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def get_viewport(self) -> Viewport:
        # if no viewport has been defined yet, you need to make one
        #   Else dpg will fail
        if not self.viewports:
            self.viewports.add(viewport := Viewport())
        else:
            # currently in dpg there is only one viewport available, but this will change in later versions
            viewport, = self.viewports
        return viewport

    # ------------------------------------------------------------------------------------------------------------------
    # - Fixes -
    # ------------------------------------------------------------------------------------------------------------------
    def fix_icon_for_taskbar(self) -> Application:
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
            # retrieve the viewport object, if it hasn't been done before, it'll set up a new one
            self.get_viewport().set_icon(icon_path=self.icon_path)

        # return itself to make these functions chainable
        return self

    # ------------------------------------------------------------------------------------------------------------------
    # - Startup and Close down -
    # ------------------------------------------------------------------------------------------------------------------
    def launch(self):
        try:
            dpg.setup_dearpygui()
            dpg.show_viewport()
            # after viewport has been show, do the post settings call
            #   as this is the only way the maximize function can be called correctly
            for callback in self.post_dpg_launchers:
                callback()

            # launching of the actual application
            dpg.start_dearpygui() # blocking call
        except KeyboardInterrupt: # made sure to do a "graceful" shutdown:
            self.graceful_minimum_shutdown()
            raise
        else:
            self.graceful_full_shutdown() # always make sure there is some form of 'graceful' shutdown

    @staticmethod
    def graceful_minimum_shutdown():
        """the bare minimum that needs to happen to make sure the shutdown is handled correctly"""
        # destroy the context, else dpg will freak out
        dpg.destroy_context()


    def graceful_full_shutdown(self):
        """the full suite of how to handle the shutdown"""
        # first do the bare minimum, which can just use the already existing function
        self.graceful_minimum_shutdown()

        # everything else is done after dpg has been shut down
        #   should handle things like dumping the settings to file
        #   etc...
        self.settings_store() # dumps the settings to file

    # ------------------------------------------------------------------------------------------------------------------
    # - Asyncio events -
    # ------------------------------------------------------------------------------------------------------------------
    def register_event(self, callback) -> asyncio.Event:
        """A way to register asyncio events, which return the event"""
        self.loop.create_task(callback(event:=asyncio.Event()))
        return event