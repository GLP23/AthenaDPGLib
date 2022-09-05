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
def update_renderable_chunks(before:bool=False):
    if before:
        def decorator_before(fnc):
            @functools.wraps(fnc)
            def wrapper(*args, **kwargs):

                Memory.chunk_manager.update_chunks_if_renderable(
                    plot_limit_min=Memory.landplot_designer.plot_limit_min,
                    plot_limit_max=Memory.landplot_designer.plot_limit_max,
                    plot_scale=Memory.landplot_designer.plot_scale,
                    plot_offset=Memory.landplot_designer.plot_offset
                )
                return fnc(*args, **kwargs)
            return wrapper
        decorator = decorator_before

    else:
        def decorator_after(fnc):
            @functools.wraps(fnc)
            def wrapper(*args, **kwargs):
                result = fnc(*args, **kwargs)

                Memory.chunk_manager.update_chunks_if_renderable(
                    plot_limit_min=Memory.landplot_designer.plot_limit_min,
                    plot_limit_max=Memory.landplot_designer.plot_limit_max,
                    plot_scale=Memory.landplot_designer.plot_scale,
                    plot_offset=Memory.landplot_designer.plot_offset
                )

                return result
            return wrapper
        decorator = decorator_after
    return decorator
