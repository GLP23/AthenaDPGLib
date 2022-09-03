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
    level_0_size:float = 2.

    # - non init vars -
    _inverse_of_level_0_size:float = field(init=False)
    _chunks:list[dict[tuple[float,float]:Chunk]] = field(init=False, default_factory=lambda:[None]*100)

    def __post_init__(self):
        self._inverse_of_level_0_size = math.pow(self.level_0_size,-1)

    def chunks(self) -> Generator[Chunk, Any, None]:
        for level_of_chunks in self._chunks: #type:dict
            if level_of_chunks is None:
                continue
            for pos,chunk in level_of_chunks.items(): # type: Point, Chunk
                if not chunk.renderable:
                    continue
                yield chunk

    def _new_chunk(self, pos:Point, level:int) -> Chunk:
        return Chunk.new_from_local(
            origin=pos.pos,
            points=(SQUARE * (self.level_0_size ** level))
        )

    def get_chunk(self, pos:Point, level:int)-> Chunk:
        pos_tuple = (pos.x, pos.y)

        if self._chunks[level] is None:
            self._chunks[level] = {pos_tuple: (chunk:=self._new_chunk(pos=pos, level=level))}
            return chunk

        elif pos_tuple in self._chunks[level]:
            return self._chunks[level][pos_tuple]

        else:
            chunk = self._new_chunk(pos=pos, level=level)
            self._chunks[level][pos_tuple] = chunk
            return chunk

    def add_landplot(self, landplot:Polygon):

        level:int = round(math.pow(landplot.largest_radius, self._inverse_of_level_0_size))

        pos = Point()
        # new_array = np.array([0.,0.]) + landplot.origin
        power = self.level_0_size**level
        calc = lambda p : power * round(p / power)

        pos._pos = np.array([calc(landplot.origin[0]), calc(landplot.origin[1])])

        chunk:Chunk = self.get_chunk(pos, level)
        chunk.land_plots.append(landplot)

