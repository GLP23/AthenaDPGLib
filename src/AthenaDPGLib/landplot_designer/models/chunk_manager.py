# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Generator
import numpy as np

# Custom Library
from AthenaLib.constants.types import NUMBER, COLOR

# Custom Packages
from AthenaDPGLib.landplot_designer.models.chunk import Chunk
from AthenaDPGLib.landplot_designer.models.land_plot import LandPlot
from AthenaDPGLib.landplot_designer.models.coordinate import Coordinate

from AthenaDPGLib.landplot_designer.data.polygon_shapes import SQUARE
from AthenaDPGLib.landplot_designer.data.chunk import ChunkSideSizes, ChunkColors


# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
CHUNK_MAPPING = dict[Coordinate:Chunk]
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class ChunkManager:
    chunks_mapping: dict[int:dict[Coordinate:Chunk]] =  field(
        default_factory=lambda : {k:{} for k, _ in enumerate(ChunkSideSizes)}
    )
    offset:np.ndarray = np.array([0.,0.])

    @property
    def chunks(self) -> Generator[Chunk, Any, None]:
        return (
            chunk #type: Chunk
            for chunk_group in self.chunks_mapping.values() #type: dict[Coordinate:Chunk]
                for _, chunk in chunk_group.items() #type: Coordinate,Chunk
        )

    def add_land_plot(self, land_plot:LandPlot):
        largest_radius:NUMBER=land_plot.largest_radius*2

        for k,(chunk_side, chunk_color) in enumerate(zip(ChunkSideSizes, ChunkColors)):
            if largest_radius <= chunk_side:
                self._assign_landplot_to_chunk(
                    land_plot=land_plot,
                    side_length=chunk_side,
                    chunk_mapping=self.chunks_mapping[k],
                    color=chunk_color
                )
                break

        # if nothing could be mapped to a known chunk size
        else:
            raise ValueError(land_plot)

    @staticmethod
    def _assign_landplot_to_chunk(land_plot:LandPlot, side_length:NUMBER, chunk_mapping:CHUNK_MAPPING, color:COLOR):
        # Calculate in which chunk the polygon should be placed in
            chunk_coord = Coordinate(
                x=(land_plot.center_coord[0] // side_length) * side_length,
                y=(land_plot.center_coord[1] // side_length) * side_length
            )

            # Assign landplot to correct chunk
            #   Create the chunk if the chunk doesn't exist yet
            if chunk_coord in chunk_mapping:
                chunk_mapping[chunk_coord].land_plots.append(land_plot)
            else:
                chunk_mapping[chunk_coord] = Chunk(
                    points=[
                        Coordinate(
                            (x * side_length) + chunk_coord.x,
                            (y * side_length) + chunk_coord.y
                        )
                        for x,y in SQUARE
                    ],
                    land_plots=[land_plot],
                    color=color
                )

    def renderable_get(self) -> Generator[Chunk, Any, None]:
        return (
            chunk #type: Chunk
            for chunk_group in self.chunks_mapping.values() #type: dict[Coordinate:Chunk]
                for chunk in chunk_group.values() #type: Coordinate,Chunk
                if chunk.renderable
        )

    def renderable_update(self, TL_limit:np.ndarray, BR_limit:np.ndarray):
        for chunk in self.chunks:
            chunk.renderable = np.logical_and(
                chunk.center_coord > TL_limit, chunk.center_coord < BR_limit
            ).all()