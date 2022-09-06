# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import functools
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.core import Core
from AthenaDPGLib.general.data.universal_tags import LandplotDebug

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def update_renderable_chunks(fnc):
    """
    Decorator which updates the boolean setting of all chunks dependent on the UI plot limits, scale and offset.
    Both `Core.chunk_manager` and `Core.designer_plot` have to be initialized before this method can be used.
    Always executes the render checks after the wrapped function has been run.
    """
    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        # Store the result to return afterwards
        result = fnc(*args, **kwargs)

        # The renderable boolean is stored on the actual chunk
        #   This means we have to go through the `Core.chunk_manager` to update these settings
        Core.chunk_manager.set_renderable_chunks(
            plot_limit_min=Core.designer_plot.plot_limit_min,
            plot_limit_max=Core.designer_plot.plot_limit_max,
            plot_scale=Core.designer_plot.plot_scale,
            plot_offset=Core.designer_plot.plot_offset
        )


        dpg.set_value(LandplotDebug.plot_offset, f"offset: {Core.designer_plot.plot_offset}")
        dpg.set_value(LandplotDebug.plot_scale, f"scale: {Core.designer_plot.plot_scale}")
        dpg.set_value(LandplotDebug.plot_limit_min, f"limit_min: {Core.designer_plot.plot_limit_min}")
        dpg.set_value(LandplotDebug.plot_limit_max, f"limit_max: {Core.designer_plot.plot_limit_max}")

        # ALWAYS MAKE SURE YOU RETURN THE RESULT!
        #   Else a decorator might have unexpected consequences
        return result
    return wrapper