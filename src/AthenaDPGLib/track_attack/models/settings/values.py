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
    show_viewport_title:bool = True

class SettingsEnum(enum.Enum):
    """
    Enum class to store all available settings in,
    Used by various systems to indirectly reference the "SettingsValues" data objects
    """
    show_viewport_title = enum.auto()