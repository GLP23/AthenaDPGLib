# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass

# Custom Library
from AthenaLib.constants.types import NUMBER, POINT

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, unsafe_hash=True)
class Coordinate:
    x:NUMBER
    y:NUMBER

    def __iter__(self):
        return iter(self.x, self.y)

    def output_to_pixelspace(self, difference_point:POINT, zero_point:POINT) -> POINT:
        """
        Output the x and y values of the current object to a tuple in pixelspace
        """
        return (
           (self.x * difference_point[0]) + zero_point[0],  # X coord
           (self.y * difference_point[1]) + zero_point[1]   # Y coord
        )