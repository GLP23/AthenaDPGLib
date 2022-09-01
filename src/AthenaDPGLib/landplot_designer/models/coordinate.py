# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Custom Library
from AthenaLib.constants.types import NUMBER

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, unsafe_hash=True)
class Coordinate:
    x:NUMBER
    y:NUMBER

    def __iter__(self):
        return iter((self.x, self.y))