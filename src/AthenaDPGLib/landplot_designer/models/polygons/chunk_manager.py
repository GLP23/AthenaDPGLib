# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Generator, Any
from dataclasses import dataclass, field
import numpy as np

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.polygons.chunk_of_polygons import ChunkOfPolygons
from AthenaDPGLib.landplot_designer.models.polygons.coordinate import Coordinate

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
CHUNK_SHAPE:np.ndarray = np.array([
    [0,0],
    [0,1],
    [1,1],
    [1,0]
])

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ChunkManager:
    chunk_side:int

    # non init
    _chunks:dict[Coordinate:ChunkOfPolygons] = field(init=False, default_factory=dict)

    @property
    def chunks(self):
        return self._chunks

    def add_chunk(self, coord:Coordinate) -> ChunkOfPolygons:
        if coord is self._chunks:
            raise ValueError(f"duplicate coord: {coord}")

        coord_true = Coordinate(
            x=coord.x * self.chunk_side,
            y=coord.y * self.chunk_side,
        )

        chunk = ChunkOfPolygons(
            point_of_origin=coord_true,
            center_point=Coordinate(
                x=coord_true.x + (self.chunk_side / 2),
                y=coord_true.y + (self.chunk_side / 2),
            )
        )

        self._chunks[coord] = chunk
        return chunk

    def renderable_get(self) -> Generator[ChunkOfPolygons, Any, None]:
        return (
            chunk_of_polygons
            for chunk_of_polygons in self.chunks.values()
            if chunk_of_polygons.renderable
        )

