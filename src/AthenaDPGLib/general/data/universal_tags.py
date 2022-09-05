# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import enum

# Custom Library

# Custom Packages
from AthenaDPGLib.general.data.constants import athena_dpg_lib_landplot_designer as adl_ld
from AthenaDPGLib.general.data.constants import athena_dpg_lib_landplot_designer_debug as adl_ldd

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class UniversalTags(enum.Enum):
    landplot_window = f"{adl_ld}_window"
    landplot_plot = f"{adl_ld}_plot"
    landplot_plot_registry = f"{adl_ld}_plot_registry"
    landplot_axis_x = f"{adl_ld}_axis_x"
    landplot_axis_y = f"{adl_ld}_axis_y"

    landplot_debug_window = f"{adl_ldd}_window"