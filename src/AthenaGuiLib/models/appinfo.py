# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

# Custom Library
from AthenaLib.models import Version

from AthenaColor import RGB, RGBA

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
    name:str="UNDEFINED"
    icon_to_taskbar:bool = True
    icon_path:str|Path = None
    version:Version = field(default_factory=Version.factory)
    min_width:int = 0
    max_width:int = 10000 #todo, maybe set this to the max width of the windows screen?
    min_height:int = 0
    max_height:int = 10000 #todo, maybe set this to the max width of the windows screen?
    resizable:bool = True
    always_on_top:bool = False
    decorated:bool=True

    @classmethod
    def factory(cls) -> AppInfo:
        return AppInfo()

    def version_to_str(self) -> str:
        """
        Returns the full version in string format
        """
        return f"{self.version.major}.{self.version.minor}.{self.version.fix}"