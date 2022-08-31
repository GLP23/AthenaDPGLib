# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygons.chunk_of_polygons import ChunkOfPolygons
from AthenaDPGLib.landplot_designer.models.polygons.coordinate import Coordinate

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ChunkManager:

    # non init
    _chunks:dict[Coordinate:ChunkOfPolygons] = field(init=False, default_factory=dict)

    @property
    def chunk(self):
        return self._chunks

    def add_chunk(self, coord:Coordinate, chunk:ChunkOfPolygons):
        if coord is self._chunks:
            self._chunks[coord] = chunk
