# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.models import Vector2D

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class _SettingsValues:
    """Value Storage, holds no logic behind the settings, only it's pure values"""
    fullscreen:bool
    maximized:bool

class _TempValues:
    """Value storage to be used for storage of info inbetween states of settings"""
    maximized_viewport_pos_size: tuple[Vector2D, Vector2D] = (Vector2D(100,100), Vector2D(600, 300))

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Settings:
    values:_SettingsValues
    _temp_values:_TempValues
    values_class:_SettingsValues = _SettingsValues
    temp_values_class:_TempValues = _TempValues
    """
    An ABC class which should be the basis for each application's Settings' class.
    Holds the update logic behind Settings, and stores the values in a separate nested class which is a TypedDict
    """

    def __init__(self, settings_dict:dict):
        self.values = self.values_class(**settings_dict)
        self._temp_values = self.temp_values_class()

    # ------------------------------------------------------------------------------------------------------------------
    # - Casting -
    # ------------------------------------------------------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Method to dump all settings to a dict format. Needs to be defined on a case by case basis"""
        return {
            slot:getattr(self.values, slot) for slot in self.values.__slots__
        }

    # ------------------------------------------------------------------------------------------------------------------
    # - Predefined Settings -
    # ------------------------------------------------------------------------------------------------------------------
    def toggle_fullscreen(self):
        # temp solution
        self.values.fullscreen = not self.values.fullscreen
        dpg.toggle_viewport_fullscreen()

    def toggle_maximize(self):
        if not self.values.maximized:
            # store information so that this can be retrieved at a later point in time
            self._temp_values.maximized_viewport_pos_size = (
                Vector2D(*dpg.get_viewport_pos()), # POSITION
                Vector2D(dpg.get_viewport_width(), dpg.get_viewport_height()), #SIZE
            )
            dpg.maximize_viewport()
        else:
            # retrieve stored information, so we can get back to where we were
            pos,size = self._temp_values.maximized_viewport_pos_size
            dpg.set_viewport_width(size.x)
            dpg.set_viewport_height(size.y)
            dpg.set_viewport_pos([pos.x, pos.y])

        # set it to the reverse of the current
        self.values.maximized = not self.values.maximized