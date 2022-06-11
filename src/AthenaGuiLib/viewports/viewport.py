# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(init=False,slots=True, unsafe_hash=True)
class Viewport:
    # ------------------------------------------------------------------------------------------------------------------
    # - Init stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        dpg.create_viewport(**kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    # - Icon -
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod # will probably eventually become a normal method, but current dpg versions only allow for one viewport
    def set_icon(*, icon_path:str):
        dpg.set_viewport_large_icon(icon_path)
        dpg.set_viewport_small_icon(icon_path)