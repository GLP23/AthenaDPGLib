# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.models.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.models.landplot_designer.memory import LandplotDesignerMemory
from AthenaDPGLib.models.landplot_designer.polygon import Polygon

from AthenaDPGLib.models.landplot_designer.components.window import Window
from AthenaDPGLib.models.landplot_designer.components.plot import Plot
from AthenaDPGLib.models.landplot_designer.components.polygon_selector import PolygonSelector

from AthenaDPGLib.data.landplot import landplot_designer_memory


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class LandplotDesigner(CustomDPGItem):
    window_tag:str
    plot_tag:str = "plot"
    polygon_selector_tag:str = "polygon_selector"

    # non init
    memory:LandplotDesignerMemory = field(init=False, default=landplot_designer_memory)
    window:Window = field(init=False)
    plot:Plot = field(init=False)
    polygon_selector:PolygonSelector = field(init=False)

    def __post_init__(self):
        self.window = Window(tag=self.window_tag)
        self.plot = Plot(tag=self.plot_tag)
        self.polygon_selector = PolygonSelector(tag=self.polygon_selector_tag)

    def constructor(self):
        with self.window.constructor():
            with dpg.group(horizontal=True):
                with self.plot.constructor():
                    pass
                with self.polygon_selector.constructor():
                    pass
