# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaLib.fixes.dataclasses import dataclass, field
from AthenaLib.constants.types import NUMBER

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
COLOR = tuple[NUMBER,NUMBER,NUMBER] | tuple[NUMBER,NUMBER,NUMBER,NUMBER]
POINT = tuple[float, float]
# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True, unsafe_hash=True)
class Polygon:
    points:tuple[Point]
    color:COLOR = field(default_factory=lambda:(0,0,0,255))
    do_render:bool = False

# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, unsafe_hash=True)
class Point:
    x:float
    y:float

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError(item)

    def output_to_pixelspace(self, difference_point:POINT, zero_point:POINT) -> POINT:
        """
        Output the x and y values of the current object to a tuple in pixelspace
        """
        return (
           (self.x * difference_point[0]) + zero_point[0],  # X coord
           (self.y * difference_point[1]) + zero_point[1]   # Y coord
        )

    def convert_to_pixelspace(self, difference_point:POINT, zero_point:POINT) -> Point:
        """
        Create a new object with the x and y values of the current object converted to pixelspace
        """
        # noinspection PyArgumentList
        return type(self)(*self.output_to_pixelspace(
            difference_point=difference_point,
            zero_point=zero_point
        ))