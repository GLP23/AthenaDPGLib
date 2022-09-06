# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaDPGLib.general.data.constants import (
    athena_dpg_lib_landplot_designer as adl_ld,
    athena_dpg_lib_landplot_designer_debug as adl_ldd,
    athena_dpg_lib_landplot_designer_settings as adl_ld_s,
    athena_dpg_lib_landplot_designer_settings_ui_plot as adl_ld_suip,
)

# ----------------------------------------------------------------------------------------------------------------------
# - LandplotDesigner components -
# ----------------------------------------------------------------------------------------------------------------------
class LandplotItems:
    viewport = None # unknown until the actual viewport is created

    window = f"{adl_ld}_window"
    plot = f"{adl_ld}_plot"
    plot_registry = f"{adl_ld}_plot_registry"
    axis_x = f"{adl_ld}_axis_x"
    axis_y = f"{adl_ld}_axis_y"

    debug_window = f"{adl_ldd}_window"

class LandplotSettings:
    settings_registry = f"{adl_ld_s}_registry"
    plot_show_chunks = f"{adl_ld_suip}_show_chunks"
    plot_show_polygons = f"{adl_ld_suip}_show_polygons"
    plot_show_origins = f"{adl_ld_suip}_show_origins"


class LandplotDebug:
    shown_chunks = f"{adl_ldd}_shown_chunks"
    shown_polygons = f"{adl_ldd}_shown_polygons"
    plot_scale = f"{adl_ldd}_plot_scale"
    plot_offset = f"{adl_ldd}_plot_offset"
    plot_limit_min = f"{adl_ldd}_plot_limit_min"
    plot_limit_max = f"{adl_ldd}_plot_limit_max"

# ----------------------------------------------------------------------------------------------------------------------
# - Internal check for duplicates -
# ----------------------------------------------------------------------------------------------------------------------
_mem:dict[str:tuple[object, str]] = {}

for obj in (LandplotItems, LandplotSettings, LandplotDebug):
    for key, val in obj.__dict__.items():
        # Skip dunders of the object and unique cases of dpg item tags which are created on startup (see viewports)
        if key.startswith("__") or val is None:
            continue
        elif val in _mem:
            raise ValueError( f"duplicate item name of {val!r} mapped to both:\n({obj}, {key!r})\n{_mem[val]}")

        # temporarily store the combination
        #   makes retrieving any found duplicates a lot easier
        _mem[val] = (obj, key)

# delete the temporary dict as it is no longer needed for anything
del _mem

