# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import enum

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class SettingsValues:
    """
    Dataclass to store all the Settings values in.
    Default values are hardcoded.
    """
    viewport_show_title:bool = True
    viewport_width:int = 1000
    viewport_height:int = 1000
    viewport_x:int = 1000
    viewport_y:int = 1000
    viewport_vsync:bool = True

class SettingsEnum(enum.Enum):
    """
    Enum class to store all available settings in,
    Used by various systems to indirectly reference the "SettingsValues" data objects
    """
    viewport_show_title = enum.auto()
    viewport_width = enum.auto()
    viewport_height = enum.auto()
    viewport_x = enum.auto()
    viewport_y = enum.auto()
    viewport_vsync = enum.auto()