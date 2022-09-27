# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
import random

# Custom Library
from AthenaLib.constants.types import PATHLIKE

# Custom Packages
from AthenaDPGLib.landplot_designer.models.chunk_manager import ChunkManager
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
from AthenaDPGLib.landplot_designer.models.core import Core

from AthenaDPGLib.landplot_designer.ui.viewport import Viewport
from AthenaDPGLib.landplot_designer.ui.designer_plot import DesignerPlot
from AthenaDPGLib.landplot_designer.ui.designer_plot_debug import DesignerPlotDebug

from AthenaDPGLib.landplot_designer.functions.settings import retrieve_settings
from AthenaDPGLib.landplot_designer.functions.value_registry import populate_value_registry

from AthenaDPGLib.landplot_designer.data.shapes import SQUARE

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def _constructor_data(settings_filepath:PATHLIKE):
    # Create data which have to be generated or called from a file before functionality and ui are created
    # ------------------------------------------------------------------------------------------------------------------
    # populates a lot of global values used within the application
    #   Has to be run first as a lot of components and functions rely on these created dpg objects
    populate_value_registry()

    # After the dpg value registry has been created, the setting can be populated
    #   Else dpg will try to update values of items that don't exist yet, leading to crashes
    retrieve_settings(settings_filepath)

def _constructor_functionality():
    # Create the models that interact with the data
    # ------------------------------------------------------------------------------------------------------------------

    # chunk manager system
    Core.chunk_manager = ChunkManager()

    Core.chunk_manager.add_landplot(
        landplot=Polygon.new_from_local(
            points=SQUARE * np.array([1, 100]),
            origin=np.array([0, 0]),
        )
    )
    Core.chunk_manager.add_landplot(
        landplot=Polygon.new_from_local(
            points=SQUARE * np.array([100, 1]),
            origin=np.array([0, 0]),
        )
    )

    for i in range(10_000):
        offset_x = float(random.randint(-10_000, 10_000))
        offset_y = float(random.randint(-10_000, 10_000))

        scale_x = random.randint(1, 10_000) / 100
        scale_y = random.randint(1, 10_000) / 100

        Core.chunk_manager.add_landplot(
            landplot=Polygon.new_from_local(
                points=SQUARE * np.array([scale_x, scale_y]),
                origin=np.array([offset_x, offset_y]),
            )
        )

    i = 0
    for level_of_chunks in Core.chunk_manager._chunks.values():
        for chunk in level_of_chunks.values():
            i += 1
    print(i)

def _constructor_ui():
    # Creates the UI models
    # ------------------------------------------------------------------------------------------------------------------

    # viewport (always has to be first)
    Core.viewport = Viewport()
    Core.viewport.add_dpg()

    # landplot designer main window
    Core.designer_plot = DesignerPlot()
    Core.designer_plot.add_dpg()

    Core.designer_plot_debug = DesignerPlotDebug()
    Core.designer_plot_debug.add_dpg()

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main(settings_filepath:PATHLIKE):
    """
    Runs all the constructors in a set order of:
    1. Data
    2. Functionality
    3. UI
    """
    _constructor_data(
        settings_filepath=settings_filepath
    )
    _constructor_functionality()
    _constructor_ui()
