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
from AthenaDPGLib.landplot_designer.models.chunk import Chunk
from AthenaDPGLib.landplot_designer.models.polygon import Polygon

from AthenaDPGLib.landplot_designer.data.shapes import SQUARE

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ChunkManager:
    """
    A ChunkManager is a managed collection of Chunks which in turn are stored in various levels of size.
    The size of a chunk is important to the UI rendering
        as it allows for the ability of larger-than-UI-viewport-sized-land_plots to be rendered
    """
    chunk_side_lowest:float = 2.

    # - non init vars -
    _chunks:dict[int:dict[tuple[float,float]:Chunk]] = field(init=False, default_factory=dict)

    # ------------------------------------------------------------------------------------------------------------------
    # - Methods for Chunk Renderable getting and setting -
    # ------------------------------------------------------------------------------------------------------------------
    def get_renderable_chunks(self) -> Generator[Chunk, Any, None]:
        """
        Generator which returns all chunks that are known to be renderable
        """
        # TODO
        #   Find a better solution to retrieve only the chunks that are currently supposed to visible
        #   Might need to depend on the chunk coord? (which is the key value of `level_of_chunks`)
        #   Then it will have to become a cross object function or a UI only component

        # Temporary solution:
        #   Loop over all chunks and check for the boolean setting
        #   Not a perfect solution
        for level_of_chunks in self._chunks.values(): #type: dict
            for chunk in level_of_chunks.values(): # type: Chunk
                if chunk.renderable:
                    yield chunk

    def set_renderable_chunks(self, plot_limit_min:ArrayLike, plot_limit_max:ArrayLike, plot_scale:float, plot_offset:ArrayLike):
        """
        Function which loops over all chunks.
        Dependent on the input arguments a chunk will be toggled renderable.
        The function is often called by user IO changes on the UI's main plot by means of a decorator.
            See: `AthenaDPGLib/landplot_designer/functions/decorators.py` -> `update_renderable_chunks`
        """
        for n,chunk_level in self.get_chunk_levels(): #type: int, dict[tuple[float,float]:Chunk]
            # Precalculate all vars that can are determined by the chunk level's size
            #   The limits are grouped as positive and negative values and not the TopLeft and BottomRight coords
            #   This makes it very easy to check if the chunk origin is between these values
            #       Instead of doing a bit more complicated math
            margin = self.chunk_side_lowest ** n
            negative_limits = (plot_limit_min - margin) * (1 / plot_scale)
            positive_limits = (plot_limit_max + margin) * (1 / plot_scale)

            for origin, chunk in chunk_level.items():
                # Again precalculate it, so it can be referenced by the logical_and check and not run twice
                offset_chunk_origin = chunk.origin + plot_offset

                # The outcome of `np.logical_and` is a boolean
                #   Meaning we can immediately use it to set the renderable flag
                chunk.renderable = np.logical_and(
                    offset_chunk_origin > negative_limits,
                    offset_chunk_origin < positive_limits
                ).all()

    # ------------------------------------------------------------------------------------------------------------------
    # - Functions to gather Chunks with specific features -
    # ------------------------------------------------------------------------------------------------------------------
    def get_chunk_levels(self)-> Generator[tuple[int, dict[tuple[float,float]:Chunk]], Any, None]:
        """
        Generator which returns all chunk_levels.
        This generator is useful if you need to go over the different sizes of chunk levels
        """
        # Loops over all chunk levels in the dictionary
        #   This is a decent solution as the amount of levels of chunks if quite limited
        #   Due to the exponential nature of chunk level sizes
        for n, level_of_chunks in self._chunks.items(): #type:dict
            yield n, level_of_chunks

    def get_chunk(self, pos: ArrayLike, level: int) -> Chunk:
        """
        Returns a Chunk object dependent on the given position and level.
        Creates new chunks if the chunk doesn't exist yet in the ChunkLevel.
        If the ChunkLevel doesn't exist then the entire level will also be created
        """
        # Get Point as a Tuple.
        #   Tuple is hashable and can be used as a key for the dictionary of chunks in a Level
        #   GIven the var is needed in all three parts of the if statement, it is created here
        pos_tuple:tuple[float, float] = (pos[0], pos[1])

        # Checks if the level is already present
        #   Creates a new ChunkLevel if it doesn't exist yet
        #   If present, then the chunk can either be retrieved dependent on the position else a new Chunk is created
        if level not in self._chunks:
            self._chunks[level] = {pos_tuple: (chunk := self._new_chunk(pos=pos, level=level))}
            return chunk
        elif pos_tuple in self._chunks[level]:
            return self._chunks[level][pos_tuple]
        else:
            self._chunks[level][pos_tuple] = (chunk := self._new_chunk(pos=pos, level=level))
            return chunk

    def _new_chunk(self, pos:ArrayLike, level:int) -> Chunk:
        """
        Simple function to create a new Chunk.
        The Chunk shape is always a perfect square
        """
        return Chunk.new_from_absolute(
            points=(SQUARE * (self.chunk_side_lowest ** level)) + pos
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Functions to gather Chunks with specific features -
    # ------------------------------------------------------------------------------------------------------------------
    def add_landplot(self, landplot:Polygon):
        """
        Adds a land plot
        :param landplot:
        :return:
        """
        # THANKS TO THE GIRLFRIEND FOR FIXING THIS FUNCTION!!!
        chunk_level = int(math.log2(math.ceil(landplot.largest_radius / self.chunk_side_lowest) * self.chunk_side_lowest)) + 1
        chunk_side = self.chunk_side_lowest ** chunk_level

        # Get the chunk
        #   after the chunk has been gathered (or created)
        #   The landplot can be added to the chunk
        chunk:Chunk = self.get_chunk(
            pos=chunk_side * (landplot.origin / chunk_side),
            level=chunk_level
        )
        chunk.land_plots.append(landplot)
