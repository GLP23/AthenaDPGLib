# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from contextlib import contextmanager

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
    # - designer tags -
    # ------------------------------------------------------------------------------------------------------------------
    plot_tag:str = NOTHING
    plot_axis_y_tag:str = NOTHING

    # ------------------------------------------------------------------------------------------------------------------
    # - POLYGONS -
    # ------------------------------------------------------------------------------------------------------------------
    polygons: dict[str:Polygon] = field(default_factory=dict)
    polygon_selected_name:str = NOTHING
    polygons_paused_render:bool = False

    def polygon_add(self, polygon:Polygon):
        if polygon.name in self.polygons:
            raise ValueError(f"duplicate polygon:\n{polygon}")

        self.polygons[polygon.name] = polygon

    def polygon_remove(self, polygon):
        if polygon.name not in self.polygons:
            raise ValueError(f"polygon not found:\n{polygon}")

        self.polygons.pop(polygon.name)

    @property
    def polygon_selected(self) -> Polygon|False:
        if self.polygon_selected_name:
            return self.polygons[self.polygon_selected_name]
        return False

    @contextmanager
    def polygons_pause_render(self):
        self.polygons_paused_render = True
        yield None
        self.polygons_paused_render = False