# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from dataclasses import dataclass, field, InitVar
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaDPGLib.models.dpg_component import DpgComponent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class Button(DpgComponent):
    label:str=NOTHING
    width:int=0
    # non init

    def __post_init__(self):
        with dpg.stage() as stage:
            self.id = dpg.add_button(
            label=self.label,
            callback=self.callback,
            width=self.width
        )
        self.stage = stage

    def dpg_raw(self):
        return

    def callback(self):
        pass

