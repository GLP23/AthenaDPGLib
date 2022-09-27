# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
from AthenaDPGLib.landplot_designer.data.shapes import SQUARE


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def polygon__square(origin:np.ndarray) -> Polygon:
    """
    Creates a Plottable Square polygon which can be displayed on the designer_plot's Plot item
    """
    return Polygon.new_from_local(origin=origin, points=SQUARE)