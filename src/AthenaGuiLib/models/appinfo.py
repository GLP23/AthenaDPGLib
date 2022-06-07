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
    icon_path:str|Path|None
    version:Version

    @classmethod
    def factory(cls) -> AppInfo:
        return AppInfo(
            name="UNDEFINED",
            icon_path=None,
            version=Version(
                major=0,
                minor=0,
                fix=0
            )
        )
