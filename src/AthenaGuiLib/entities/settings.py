# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

# Custom Library
from AthenaLib.models import Version

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    eq=False, # no need for equal check
    kw_only=True,
    slots=True
)
class Settings:
    """
    Application Settings class, houses all the changable information of an application
    Aka: fullscreen state, position, etc
    """
    version: Version
    name: str
    icon_path:str|Path