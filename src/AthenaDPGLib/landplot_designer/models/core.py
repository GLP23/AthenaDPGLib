# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaLib.constants.types import CV_UNDEFINED

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Core:
    # functionality
    chunk_manager: CV_UNDEFINED

    # ui
    viewport : CV_UNDEFINED
    designer_plot: CV_UNDEFINED
    designer_plot_debug: CV_UNDEFINED

    __slots__ = [
        "chunk_manager",
        "designer_plot",
        "designer_plot_debug"
    ]
