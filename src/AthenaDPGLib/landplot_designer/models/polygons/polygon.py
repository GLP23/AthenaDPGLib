# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
import math
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.constants.types import COLOR

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygons.coordinate import Coordinate

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Polygon:
    coords:list[Coordinate]
    color:COLOR = field(default_factory=lambda:(0,0,0,255))
    renderable:bool = False

    # non init
    # math stuff for checking if everything is okay to render
    points_as_array:np.ndarray = field(hash=False, init=False)
    center_point:Coordinate = field(init=False)
    largest_radius:float = field(init=False)

    def __post_init__(self):
        self.points_as_array = self._points_as_array()
        self.center_point = self._center_point()
        self.largest_radius = self._largest_radius()

    # ------------------------------------------------------------------------------------------------------------------
    # - Math operations -
    # ------------------------------------------------------------------------------------------------------------------
    def _points_as_array(self) -> np.ndarray:
        return np.array([
            [point.x, point.y]
            for point in self.coords
        ])

    def _center_point(self) -> Coordinate:
        length = len(self.coords)
        return Coordinate(
            x = self.points_as_array[:, 0].sum() / length ,
            y = self.points_as_array[:, 1].sum() / length
        )

    def _largest_radius(self) -> float:
        """
        Find the distance between the center point and the outer coords.
            This will give all the radia
            Which in turn allows us to find the largest
        """
        return np.amax(
            np.array([
                math.sqrt(math.pow(self.center_point.x - x, 2) + math.pow(self.center_point.y - y, 2))
                for x, y in self.points_as_array
            ]),
            axis=0
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Other methods -
    # ------------------------------------------------------------------------------------------------------------------
    def renderable_update(self, x_limit0, x_limit1, y_limit0, y_limit1):
        self.renderable:bool = (
            (x_limit0-self.largest_radius) < self.center_point.x < (x_limit1+self.largest_radius) and
            (y_limit0-self.largest_radius) < self.center_point.y < (y_limit1+self.largest_radius)
        )


