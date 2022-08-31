# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Generator, Any
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygons.polygon import Polygon

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ChunkOfPolygons:
    _collection:list[Polygon] = field(init=False, default_factory=list)

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


# --