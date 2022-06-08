# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg
from pathlib import Path

# Custom Library
from AthenaColor import RGBA

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Viewport:
    title: str = "UNDEFINED"
    icon_path: str | Path = None
    min_width: int = 0
    max_width: int = 10000  # todo, maybe set this to the max width of the windows screen?
    min_height: int = 0
    max_height: int = 10000  # todo, maybe set this to the max width of the windows screen?
    resizable: bool = True
    always_on_top: bool = False
    decorated: bool = True
    fullscreen: bool = False
    vsync:bool = True
    background_color: RGBA = RGBA(0,0,0,255)

    def __init__(self):
        # nothing else so far, as there is no possibitly for multiple viewports
        # maybe in dpg 2.0 this will be usefull
        dpg.create_viewport()
