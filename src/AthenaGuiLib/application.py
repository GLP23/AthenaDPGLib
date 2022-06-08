# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Callable

# Custom Library
from AthenaLib.models import Version

# Custom Packages
from AthenaGuiLib.controllers import ViewportController, WindowController
from AthenaGuiLib.entities import Settings

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True, eq=False)
class Application:
    # hard coded stuff
    version: Version
    name: str
    icon_path: str | Path

    settings_json_path:str|Path = None
    settings_handlers:dict[int:Callable] = field(default_factory=dict)

    # items and content
    windows:dict[int:WindowController] = field(default_factory=dict)

    # all the bellow attributes are not to be setup with the init
    viewport:ViewportController=field(init=False)

    settings:Settings=field(init=False)

    restart:bool=field(init=False, default=True)


    # ------------------------------------------------------------------------------------------------------------------
    # - Init -
    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        # NEEDS TO BE FIRST!
        dpg.create_context()
        # Put all othert stuff below here in correct order
        self.viewport = ViewportController()

    def setup_settings(self) -> Application:
        # import settings if they are present
        if self.settings_json_path is not None:
            with open(self.settings_json_path, "r") as settings_file:
                settings_dict = json.load(settings_file)
                try:
                    settings_version = settings_dict["Version"]
                    settings_content = settings_dict["Content"]
                except KeyError:
                    raise KeyError("Settings json file was incorrectly formatted, did not hold a 'SettingsVersion' key")

            # parse and store settings
            if settings_version not in self.settings_handlers:
                raise KeyError("No setting handler found")
            self.settings_handlers[settings_version](content=settings_content)
        return self

    def setup_viewport(self) -> Application:
        # at the end of the post_init, populate the viewport with all the available settings
        self.viewport.title = self.name
        self.viewport.set_icon(icon_path=self.icon_path,ModelID=f"{self.name}[{self.version}]")

        return self

    # ------------------------------------------------------------------------------------------------------------------
    # - Settings Handlers -
    # ------------------------------------------------------------------------------------------------------------------
    def add_setting_handler(self, version, fnc:Callable) -> Application:
        if version in self.settings_handlers:
            raise KeyError("No duplicate handlers allowed")
        self.settings_handlers[version] = fnc
        return self

    # ------------------------------------------------------------------------------------------------------------------
    # - Content Handlers -
    # ------------------------------------------------------------------------------------------------------------------
    def add_window(self, window: WindowController):
        window.assemble()
        self.windows[window.id] = window



    # ------------------------------------------------------------------------------------------------------------------
    # - DPG related Methods -
    # ------------------------------------------------------------------------------------------------------------------
    def launch(self):
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