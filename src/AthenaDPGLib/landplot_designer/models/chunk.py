# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygon import Polygon

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Chunk(Polygon):
    """
    A chunk is a container for multiple land_plots.
    A Chunk's position is used to determine the rentability of it's land_plots.
        This calculation is done by the ChunkManager and is dependent on the LandplotDesigner's UI constraints.
    """

    renderable:bool = False
    land_plots:list[Polygon] = field(init=False, default_factory=list)