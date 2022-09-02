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

    def renderable_update(self, x_limit0, x_limit1, y_limit0, y_limit1):
        self.renderable:bool = (
            (x_limit0-self.largest_radius) < self.center_coord.x < (x_limit1+self.largest_radius) and
            (y_limit0-self.largest_radius) < self.center_coord.y < (y_limit1+self.largest_radius)
        )