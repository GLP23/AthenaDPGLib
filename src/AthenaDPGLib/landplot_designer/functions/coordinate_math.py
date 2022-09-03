# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import math
import numpy as np

# Custom Library
from AthenaLib.constants.types import NUMBER

# Custom Packages
from AthenaDPGLib.landplot_designer.models.coordinate import Coordinate

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def array_of_coords(coords:list[Coordinate]) -> np.ndarray:
    return np.array([
        [coord.x, coord.y]
        for coord in coords
    ])

def calculate_distance_between_two_coords(coord1:np.ndarray, coord2:Coordinate) -> NUMBER:
    return math.sqrt(math.pow(coord1[0] - coord2.x, 2) + math.pow(coord1[1] - coord2.y, 2))

def calculate_largest_radius(center_coord:np.ndarray, outside_coords:list[Coordinate]) -> NUMBER:
    return np.amax(
        np.array([
            calculate_distance_between_two_coords(center_coord, coord)
            for coord in outside_coords
        ]),
        axis=0
    )

def calculate_center_coord(coords:np.ndarray) -> np.ndarray:
    return np.array([
        coords[:, 0].sum() / (length := len(coords)) ,
        coords[:, 1].sum() / length
    ])