# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
from AthenaDPGLib.landplot_designer.models.point import Point


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def polygon__square(origin:np.ndarray) -> Polygon:
    return Polygon.new_from_local(origin=origin, points=np.array([
        [-.5, -.5],
        [-.5,  .5],
        [.5 ,  .5],
        [.5 , -.5]
    ]))