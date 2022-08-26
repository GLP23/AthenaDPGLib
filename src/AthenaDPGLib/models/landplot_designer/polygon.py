# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.data.types import NUMBER

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Polygon:
    name:str
    points:list[int] = field(default_factory=list)
    color:list[NUMBER] = field(default_factory=lambda : [0,0,0,255])