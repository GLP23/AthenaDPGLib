# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaLib.constants.types import POINT

# Custom Packages
from AthenaDPGLib.landplot_designer.models.coordinate import Coordinate

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def tuple_to_pixelspace(original:POINT, difference_point: POINT, zero_point: POINT) -> POINT:
    """
    Output the x and y values of the current object to a tuple in pixelspace
    """
    return (
            (original[0] * difference_point[0]) + zero_point[0] ,
            (original[1] * difference_point[1]) + zero_point[1]
    )

def coord_to_pixelspace(original:Coordinate, difference_point: POINT, zero_point: POINT) -> POINT:
    """
    Output the x and y values of the current object to a tuple in pixelspace
    """
    return (
            (original.x * difference_point[0]) + zero_point[0] ,
            (original.y * difference_point[1]) + zero_point[1]
    )