# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg
import numpy as np

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
from AthenaDPGLib.landplot_designer.models.land_plot import LandPlot
from AthenaDPGLib.landplot_designer.models.coordinate import Coordinate

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Chunk(Polygon):
    renderable:bool = False
    land_plots:list[LandPlot] = field(default_factory=list)

    # non init
    largest_radius_doubled:int|float = field(init=False)
    def __post_init__(self):
        super(Chunk, self).__post_init__()

        # Possible because the radius of a chunk doesn't change sizes
        #   A chunk is of a set size and will never change its shape
        self.largest_radius_doubled = self.largest_radius*2