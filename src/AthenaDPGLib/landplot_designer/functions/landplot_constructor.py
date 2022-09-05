# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import random

import numpy as np

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.ui.landplot_designer import LandplotDesigner

from AthenaDPGLib.landplot_designer.models.chunk_manager import ChunkManager
from AthenaDPGLib.landplot_designer.models.point import Point
from AthenaDPGLib.landplot_designer.models.polygon import Polygon

import AthenaDPGLib.landplot_designer.data.memory as Memory
from AthenaDPGLib.landplot_designer.data.shapes import SQUARE

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def landplot_constructor():
    """
    Main function of the landplot designer tool.
    It creates all objects in the right, so they can be used by all components.
    The DPG context has to be created for this to work
    """
    # Create data which have to be generated
    # ------------------------------------------------------------------------------------------------------------------

    # Create the models that interact with the data
    # ------------------------------------------------------------------------------------------------------------------

    # chunk manager system
    Memory.chunk_manager = ChunkManager()
    for i in range(1_000):
        offset_x = float(random.randint(-10_000, 10_000))
        offset_y = float(random.randint(-10_000, 10_000))

        scale_x = float(random.randint(1, 100))
        scale_y = float(random.randint(1, 100))

        Memory.chunk_manager.add_landplot(
            landplot=Polygon.new_from_local(
                points=SQUARE*np.array([scale_x,scale_y]),
                origin=np.array([offset_x,offset_y]),
            )
        )

    # Create the UI
    # ------------------------------------------------------------------------------------------------------------------

    # landplot designer main window
    Memory.landplot_designer = LandplotDesigner()
    Memory.landplot_designer.add_dpg()