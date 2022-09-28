# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg
import pathlib
import json
from typing import Any

# Custom Library
from AthenaLib.constants.types import PATHLIKE

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Settings:
    json_file:PATHLIKE

    # non init
    show_viewport_titlebar:bool=field(init=False, default=True)

    def load_from_file(self):
        # Load from file
        #   If the file doesn't exist, use some form of "default" settings
        if not pathlib.Path(self.json_file).exists():
            return

        with open(self.json_file) as file:
            loaded_settings: dict = json.load(file)

        for key, value in loaded_settings: #type: str, Any
            setattr(self, key, value)


    def dump_to_file(self):
        pass