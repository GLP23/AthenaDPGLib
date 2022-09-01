# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.coordinate import Coordinate

from AthenaDPGLib.landplot_designer.functions.coordinate_math import (
    calculate_largest_radius,
    calculate_center_coord,
    array_of_coords
)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Polygon:
    coords:list[Coordinate]
    renderable:bool = False

    # non init
    # math stuff for checking if everything is okay to render
    coords_as_np_array:np.ndarray = field(hash=False, init=False)
    center_coord:Coordinate = field(init=False)
    largest_radius:float = field(init=False)

    def __post_init__(self):
        self.coords_as_np_array = array_of_coords(coords=self.coords)
        self.center_coord = calculate_center_coord(coords=self.coords_as_np_array)
        self.largest_radius = calculate_largest_radius(center_coord=self.center_coord, outside_coords=self.coords)

   # ------------------------------------------------------------------------------------------------------------------
    # - Other methods -
    # ------------------------------------------------------------------------------------------------------------------
    def renderable_update(self, x_limit0, x_limit1, y_limit0, y_limit1):
        self.renderable:bool = (
                (x_limit0-self.largest_radius) < self.center_coord.x < (x_limit1 + self.largest_radius) and
                (y_limit0-self.largest_radius) < self.center_coord.y < (y_limit1 + self.largest_radius)
        )


