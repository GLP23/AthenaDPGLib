# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import functools

# Custom Library

# Custom Packages
import AthenaDPGLib.landplot_designer.data.memory as Memory

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def update_renderable_chunks(fnc):
    """
    Decorator which updates the boolean setting of all chunks dependent on the UI plot limits, scale and offset.
    Both `Memory.chunk_manager` and `Memory.landplot_designer` have to be initialized before this method can be used.
    Always executes the render checks after the wrapped function has been run.
    """
    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        # Store the result to return afterwards
        result = fnc(*args, **kwargs)

        # The renderable boolean is stored on the actual chunk
        #   This means we have to go through the `Memory.chunk_manager` to update these settings
        Memory.chunk_manager.set_renderable_chunks(
            plot_limit_min=Memory.landplot_designer.plot_limit_min,
            plot_limit_max=Memory.landplot_designer.plot_limit_max,
            plot_scale=Memory.landplot_designer.plot_scale,
            plot_offset=Memory.landplot_designer.plot_offset
        )

        # ALWAYS MAKE SURE YOU RETURN THE RESULT!
        #   Else a decorator might have unexpected consequences
        return result
    return wrapper