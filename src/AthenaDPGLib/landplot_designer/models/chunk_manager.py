# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Generator

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.chunk import Chunk
from AthenaDPGLib.landplot_designer.models.land_plot import LandPlot
from AthenaDPGLib.landplot_designer.models.coordinate import Coordinate

from AthenaDPGLib.landplot_designer.data.polygon_shapes import SQUARE

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class ChunkManager:
    chunk_side_length:int

    chunks:dict[Coordinate:Chunk] = field(init=False,default_factory=dict)

    def add_land_plot(self, land_plot:LandPlot):
        # Calculate in which chunk the polygon should be placed in
        chunk_coord = Coordinate(
            x=(land_plot.center_coord.x // self.chunk_side_length)*self.chunk_side_length,
            y=(land_plot.center_coord.y // self.chunk_side_length)*self.chunk_side_length
        )


        # Assign landplot to correct chunk
        #   Create the chunk if the chunk doesn't exist yet
        if chunk_coord in self.chunks:
            self.chunks[chunk_coord].land_plots.append(land_plot)
        else:
            self.chunks[chunk_coord] = Chunk(
                points=[
                    Coordinate(
                        (x*self.chunk_side_length)+chunk_coord.x,
                        (y*self.chunk_side_length)+chunk_coord.y
                    )
                    for x,y in SQUARE
                ],
                land_plots=[land_plot]
            )

    def renderable_get(self) -> Generator[Chunk, Any, None]:
        return (
            chunk
            for coord, chunk in self.chunks.items() #type: Coordinate,Chunk
            if chunk.renderable
        )