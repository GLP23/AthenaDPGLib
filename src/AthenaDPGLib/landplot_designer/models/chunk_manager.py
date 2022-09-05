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

    def renderable_chunks(self) -> Generator[Chunk, Any, None]:
        for level_of_chunks in self._chunks.values(): #type: dict
            for chunk in level_of_chunks.values(): # type: Chunk
                if chunk.renderable:
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

    def update_chunks_if_renderable(
            self, plot_limit_min:ArrayLike, plot_limit_max:ArrayLike, plot_scale:float, plot_offset:ArrayLike
    ):
        for n,chunk_level in self.chunk_levels(): #type: int, dict[tuple[float,float]:Chunk]

            margin = self.chunk_side_lowest ** n

            TL_limit_margin = (plot_limit_min - margin ) * (1/plot_scale)
            BR_limit_margin = (plot_limit_max + margin ) * (1/plot_scale)

            for origin, chunk in chunk_level.items():
                offset_chunk_origin = chunk.origin + plot_offset

                chunk.renderable = np.logical_and(
                    offset_chunk_origin > TL_limit_margin,
                    offset_chunk_origin < BR_limit_margin
                ).all()
