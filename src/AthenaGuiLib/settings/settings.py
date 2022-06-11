# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import NamedTuple
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.models import Vector2D

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
class _SettingsValues(NamedTuple):
    """Value Storage, holds no logic behind the settings, only it's pure values"""
    fullscreen:bool
    maximized:bool

class _TempValues:
    """Value storage to be used for storage of info inbetween states of settings"""
    maximized_viewport_pos_size: tuple[Vector2D, Vector2D]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(init=False, slots=True)
class Settings:
    _values:_SettingsValues
    _temp_values:_TempValues
    values_class:_SettingsValues = _SettingsValues
    temp_values_class:_TempValues = _TempValues
    """
    An ABC class which should be the basis for each application's Settings' class.
    Holds the update logic behind Settings, and stores the values in a separate nested class which is a TypedDict
    """

    def __init__(self, settings_dict:dict):
        self._values = self.values_class(**settings_dict)
        self._temp_values = self.temp_values_class()

    def to_dict(self):
        """Method to dump all settings to a dict format. Needs to be defined on a case by case basis"""
        return self._values._asdict()

    # ------------------------------------------------------------------------------------------------------------------
    # - Predefined Settings -
    # ------------------------------------------------------------------------------------------------------------------
    def toggle_fullscreen(self):
        dpg.toggle_viewport_fullscreen()

    def toggle_maximize(self):
        if not self._values.maximized:
            # store information so that this can be retrieved at a later point in time
            self._temp_values.maximized_viewport_pos_size = (
                Vector2D(*dpg.get_viewport_pos()), # POSITION
                Vector2D(dpg.get_viewport_width(), dpg.get_viewport_height()), #SIZE
            )
            dpg.maximize_viewport()
        else:
            # retrieve stored information, so we can get back to where we were
            pos,size = self._temp_values.maximized_viewport_pos_size
            dpg.set_viewport_pos([pos.x, pos.y])
            dpg.set_viewport_width(size.x)
            dpg.set_viewport_height(size.y)

        # set it to the reverse of the current
        self._values.maximized = not self._values.maximized