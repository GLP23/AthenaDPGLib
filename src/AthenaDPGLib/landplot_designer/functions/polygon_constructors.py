# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
from typing import Any, Generator

# Custom Library
from AthenaColor.data.colors_html import GOLD

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon


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

def test_polygons() -> Generator[Polygon, Any, None]:
    yield polygon__square(origin=np.array([0.5, 0.5]))
    yield polygon__square(origin=np.array([1., 1.]))
    yield polygon__square(origin=np.array([1., 5.]))
    yield polygon__square(origin=np.array([-5.,2.]))
    yield Polygon.new_from_absolute(
        points=np.array([
            [5., -5.],
            [5., -2.5],
            [2.5, -2.5],
            [2.5, -5.]
        ]),
        color_fill=GOLD,
        color_border=GOLD
    )
