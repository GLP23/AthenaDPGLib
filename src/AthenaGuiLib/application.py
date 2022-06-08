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

# Custom Packages
from AthenaGuiLib.controllers import ViewportController
from AthenaGuiLib.entities import Settings

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True, eq=False)
class Application:
    settings_json_path:str|Path = None
    settings_handlers:dict[int:Callable] = field(default_factory=dict)

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

    def setup(self) -> Application:
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
            self.settings = self._handle_settings(settings_version, settings_content)
        return self

    def setup_viewport(self) -> Application:
        # at the end of the post_init, populate the viewport with all the available settings
        self.viewport.title = self.settings.name
        self.viewport.set_icon(icon_path=self.settings.icon_path,ModelID=f"{self.settings.name}[{self.settings.version}]")

        return self

    # ------------------------------------------------------------------------------------------------------------------
    # - Settings Handlers -
    # ------------------------------------------------------------------------------------------------------------------
    def add_setting_handler(self, version, fnc:Callable) -> Application:
        if version in self.settings_handlers:
            raise KeyError("No duplicate handlers allowed")
        self.settings_handlers[version] = fnc

        return self

    def _handle_settings(self, settings_version:int, content=dict) -> Settings:
        if settings_version not in self.settings_handlers:
            raise KeyError("No setting handler found")
        return self.settings_handlers[settings_version](content=content)

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
            # else, the restart option is set, and this will allow for a new application startup