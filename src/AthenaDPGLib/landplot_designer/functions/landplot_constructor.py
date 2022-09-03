# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.ui.landplot_designer import LandplotDesigner
from AthenaDPGLib.landplot_designer.models.chunk_manager import ChunkManager

import AthenaDPGLib.landplot_designer.data.memory as Memory

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

    # Create the UI
    # ------------------------------------------------------------------------------------------------------------------

    # landplot designer main window
    Memory.landplot_designer = LandplotDesigner()
    Memory.landplot_designer.add_dpg()