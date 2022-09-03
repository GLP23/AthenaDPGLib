# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.point import Point
from AthenaDPGLib.landplot_designer.models.chunk import Chunk

from AthenaDPGLib.landplot_designer.functions.constructors import chunk_manager__chunks

from AthenaDPGLib.landplot_designer.data.constants import CHUNK_LEVELS

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ChunkManager:
    chunk_side_size:int = 16


    # - non init vars -
    _chunks:dict[int:dict[Point:Chunk]] = field(init=False, default_factory=chunk_manager__chunks)

    def _calculate_chunk_level(self,pos:Point) -> CHUNK_LEVELS:
        """
        Calculation depends on two factors:
        - The position of the original object
        - The largest radius size of the original object
        """

    def _add_chunk(self, pos:Point, level:CHUNK_LEVELS):
        # chunk cannot exist already inside the chunks dictionary
        if pos in self._chunks[level]:
            raise ValueError(f"Chunk position ({pos=}) was already occupied at {level=}")

        self._chunks[level][pos] = Chunk()
