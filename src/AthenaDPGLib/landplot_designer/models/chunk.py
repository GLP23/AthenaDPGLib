# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
from AthenaDPGLib.landplot_designer.models.land_plot import LandPlot

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

    def renderable_update(self, x_limit0, x_limit1, y_limit0, y_limit1):
        self.renderable:bool = (
            (x_limit0-self.largest_radius_doubled) < self.center_coord.x < (x_limit1+self.largest_radius_doubled) and
            (y_limit0-self.largest_radius_doubled) < self.center_coord.y < (y_limit1+self.largest_radius_doubled)
        )