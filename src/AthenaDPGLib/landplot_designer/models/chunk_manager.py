# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import copy
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import ArrayLike
from typing import Generator, Any
import math

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.point import Point
from AthenaDPGLib.landplot_designer.models.chunk import Chunk
from AthenaDPGLib.landplot_designer.models.polygon import Polygon

from AthenaDPGLib.landplot_designer.data.shapes import SQUARE

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ChunkManager:
    chunk_side_lowest:float = 2.

    # - non init vars -
    _inverse_of_level_0_size:float = field(init=False)
    _chunks:dict[int:dict[tuple[float,float]:Chunk]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self._inverse_of_level_0_size = math.pow(self.chunk_side_lowest, -1)

    def chunks(self) -> Generator[Chunk, Any, None]:
        for level_of_chunks in self.chunk_levels(): #type:dict
            for pos,chunk in level_of_chunks.items(): # type: Point, Chunk
                if not chunk.renderable:
                    continue
                yield chunk

    def chunk_levels(self)-> Generator[tuple[int, dict[tuple[float,float]:Chunk]], Any, None]:
        for n, level_of_chunks in self._chunks.items(): #type:dict
            yield n, level_of_chunks

    def _new_chunk(self, pos:Point, level:int) -> Chunk:
        return Chunk.new_from_absolute(
            points=(SQUARE * (self.chunk_side_lowest ** level)) + pos.pos
        )

    def get_chunk(self, pos:Point, level:int)-> Chunk:
        pos_tuple = (pos.x, pos.y)

        if level not in self._chunks:
            self._chunks[level] = {pos_tuple: (chunk:=self._new_chunk(pos=pos, level=level))}
            return chunk

        elif pos_tuple in self._chunks[level]:
            return self._chunks[level][pos_tuple]

        else:
            chunk = self._new_chunk(pos=pos, level=level)
            self._chunks[level][pos_tuple] = chunk
            return chunk


    def add_landplot(self, landplot:Polygon):
        level = int(math.log2(math.ceil(landplot.largest_radius / self.chunk_side_lowest) * self.chunk_side_lowest)) + 1

        power = self.chunk_side_lowest ** level
        calc = lambda p : power * round(p / power)

        pos = Point.from_array(
            np.array(
                [calc(landplot.origin[0]), calc(landplot.origin[1])]
            )
        )

        chunk:Chunk = self.get_chunk(pos, level)
        chunk.land_plots.append(landplot)

