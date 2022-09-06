# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import numpy as np
import random

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.chunk_manager import ChunkManager
from AthenaDPGLib.landplot_designer.models.polygon import Polygon
from AthenaDPGLib.landplot_designer.models.core import Core

from AthenaDPGLib.landplot_designer.ui.designer_plot import DesignerPlot
from AthenaDPGLib.landplot_designer.ui.designer_plot_debug import DesignerPlotDebug

from AthenaDPGLib.landplot_designer.data.shapes import SQUARE

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def _constructor_data():
    # Create data which have to be generated or called from a file before functionality and ui are created
    # --------------------------------------------------------------------------------------------------------------
    pass

def _constructor_functionality():
    # Create the models that interact with the data
    # --------------------------------------------------------------------------------------------------------------

    # chunk manager system
    Core.chunk_manager = ChunkManager()
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

def _constructor_ui():
    # Creates the UI models
    # --------------------------------------------------------------------------------------------------------------

    # landplot designer main window
    Core.designer_plot = DesignerPlot()
    Core.designer_plot.add_dpg()

    Core.designer_plot_debug = DesignerPlotDebug()
    Core.designer_plot_debug.add_dpg()

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    _constructor_data()
    _constructor_functionality()
    _constructor_ui()
