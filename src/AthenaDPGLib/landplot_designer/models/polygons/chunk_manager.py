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
        print(coord_true)

        chunk = ChunkOfPolygons(
            point_of_origin=coord_true,
            center_point=self._chunk_center_point(
                point_of_origin=np.array([[coord.x * self.chunk_side, coord.y * self.chunk_side]])
            )
        )

        self._chunks[coord] = chunk
        return chunk

    def renderable_get(self) -> Generator[ChunkOfPolygons, Any, None]:
        return (
            chunk_of_polygons
            for chunk_of_polygons in self._chunks.values()
            if chunk_of_polygons.renderable
        )

    def _chunk_center_point(self, point_of_origin:np.array) -> Coordinate:
        chunk_shape:np.ndarray = (CHUNK_SHAPE + point_of_origin)
        print(chunk_shape)
        return Coordinate(
            x=chunk_shape[:, 0].sum() / 4,
            y=chunk_shape[:, 1].sum() / 4
        )

