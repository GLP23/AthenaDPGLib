# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
import math

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

    # non init
    # math stuff for checking if everything is okay to render
    points_as_array:np.ndarray = field(hash=False, init=False)
    center_point:Point = field(init=False)
    largest_radius:float = field(init=False)

    def __post_init__(self):
        self.points_as_array = self._points_as_array()
        self.center_point = self._center_point()
        self.largest_radius = self._largest_radius()

    def _points_as_array(self) -> np.ndarray:
        return np.array(
            [[point.x, point.y] for point in self.points]
        )

    def _center_point(self) -> Point:
        length = len(self.points)
        return Point(
            x = self.points_as_array[:, 0].sum() / length ,
            y = self.points_as_array[:, 1].sum() / length
        )

    def _largest_radius(self) -> float:
        return np.amax(
            np.array(
                [
                    math.sqrt(math.pow(self.center_point.x - x, 2) + math.pow(self.center_point.y - y, 2))
                    for x, y in self.points_as_array
                ]
            ),
            axis=0
        )

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

    def export(self):
        return self.x, self.y

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