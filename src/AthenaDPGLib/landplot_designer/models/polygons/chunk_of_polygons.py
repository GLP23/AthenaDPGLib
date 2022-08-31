# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Generator, Any
from dataclasses import dataclass, field
import math

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygons.polygon import Polygon
from AthenaDPGLib.landplot_designer.models.polygons.coordinate import Coordinate

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ChunkOfPolygons:
    point_of_origin:Coordinate
    center_point:Coordinate
    renderable:bool = False
    _collection:list[Polygon] = field(init=False, default_factory=list)
    _largest_radius:float = field(init=False)

    def __post_init__(self):
        self._largest_radius = math.sqrt(
            math.pow(self.center_point.x - self.point_of_origin.x, 2)
            + math.pow(self.center_point.y - self.point_of_origin.y, 2)
        )

    @property
    def collection(self):
        return self._collection

    def append(self, polygon:Polygon):
        self._collection.append(polygon)

    def clear(self) -> None:
        self._collection.clear()

    def renderable_get(self) -> Generator[Polygon, Any, None]:
        return (
            polygon
            for polygon in self._collection
            if polygon.renderable
        )

    def renderable_update(self, x_limit0, x_limit1, y_limit0, y_limit1):
        # print(x_limit0-self._largest_radius , self.center_point.x, x_limit1+self._largest_radius)
        self.renderable:bool = (
            (x_limit0-self._largest_radius) < self.center_point.x < (x_limit1+self._largest_radius) and
            (y_limit0-self._largest_radius) < self.center_point.y < (y_limit1+self._largest_radius)
        )