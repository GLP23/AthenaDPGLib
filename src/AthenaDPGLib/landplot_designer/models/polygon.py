# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.constants.types import COLOR

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
    points:list[Coordinate] = field(default_factory=list)
    color:COLOR = field(default_factory=lambda:(0,0,0,255))

    # non init
    # math stuff for checking if everything is okay to render
    points_as_np_array:np.ndarray = field(init=False)
    center_coord:np.ndarray = field(init=False)
    largest_radius:float = field(init=False)

    def __post_init__(self):
        self.update_coords()

    def update_coords(self):
        """
        Collection of math operations that need to be run when a coord of the polygon changes
        """
        self.points_as_np_array = array_of_coords(coords=self.points)
        self.center_coord = calculate_center_coord(coords=self.points_as_np_array)
        self.largest_radius = calculate_largest_radius(center_coord=self.center_coord, outside_coords=self.points)

