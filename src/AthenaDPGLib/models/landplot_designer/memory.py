# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaDPGLib.models.landplot_designer.polygon import Polygon

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class LandplotDesignerMemory:
    # ------------------------------------------------------------------------------------------------------------------
    # - POLYGONS -
    # ------------------------------------------------------------------------------------------------------------------
    polygons: dict[str:Polygon] = field(default_factory=dict)
    selected_polygon:str = NOTHING

    def polygons_add(self, polygon:Polygon):
        if polygon.name in self.polygons:
            raise ValueError(f"duplicate polygon:\n{polygon}")

        self.polygons[polygon.name] = polygon

    def polygons_remove(self, polygon):
        if polygon.name not in self.polygons:
            raise ValueError(f"polygon not found:\n{polygon}")

        self.polygons.pop(polygon.name)
