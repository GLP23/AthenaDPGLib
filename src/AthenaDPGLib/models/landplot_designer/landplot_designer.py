# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.models.custom_dpg_item import CustomDPGItem
from AthenaDPGLib.models.landplot_designer.memory import LandplotDesignerMemory

from AthenaDPGLib.models.landplot_designer.components.window import LandplotDesigner_Window
from AthenaDPGLib.models.landplot_designer.components.plot import LandplotDesigner_Plot

from AthenaDPGLib.data.landplot import landplot_designer_memory

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class LandplotDesigner(CustomDPGItem):
    window_tag:str
    plot_tag:str = "plot"

    # non init
    memory:LandplotDesignerMemory = field(init=False, default=landplot_designer_memory)
    window:LandplotDesigner_Window = field(init=False)
    plot:LandplotDesigner_Plot = field(init=False)

    def __post_init__(self):
        self.window = LandplotDesigner_Window(tag=self.window_tag)
        self.plot = LandplotDesigner_Plot(tag=self.plot_tag)

    def constructor(self):
        with self.window.constructor():
            with self.plot.constructor():
                pass