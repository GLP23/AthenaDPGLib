# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

# Custom Library
from AthenaLib.models import Version

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    eq=False, # no need for equal check between two AppInfo's as there is only meant to be one per application
    frozen=True, # frozen to keep it from changing after being set
    kw_only=True,
    slots=True
)
class AppInfo:
    """
    Application Info relating to the current version, name, id, etc...
    All data is frozen after creation to make sure that the information stays the same
    """
    name:str
    icon_path:str|Path = None
    version:Version = field(default_factory=Version.factory)
    min_width:int = 0
    max_width:int = 10000 #todo, maybe set this to the max width of the windows screen?
    min_height:int = 0
    max_height:int = 10000 #todo, maybe set this to the max width of the windows screen?
    resizable:bool = True

    @classmethod
    def factory(cls) -> AppInfo:
        return AppInfo(
            name="UNDEFINED",
            # others don't need to be set to anything, as this all have default values
        )
