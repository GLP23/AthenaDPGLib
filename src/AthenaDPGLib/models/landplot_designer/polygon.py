# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import Optional

# Custom Library
from AthenaLib.data.types import NUMBER

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Polygon:
    name:str

    colors:InitVar[list[NUMBER]] = None

    points:list[int|str] = field(default_factory=list)
    color_fill:list[NUMBER] = field(default_factory=lambda : [0,0,0,255])
    color_border:list[NUMBER] = field(default_factory=lambda : [0,0,0,255])
    color_node:list[NUMBER] = field(default_factory=lambda : [0,0,0,255])
    series:Optional[str|int] = None

    def __post_init__(self, colors: list[NUMBER]):
        if colors is not None:
            self.color_fill = colors
            self.color_border = colors
            self.color_node = colors