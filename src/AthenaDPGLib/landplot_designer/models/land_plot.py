# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

# Custom Library
from AthenaLib.constants.types import COLOR

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
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
class LandPlot(Polygon):
    pass

