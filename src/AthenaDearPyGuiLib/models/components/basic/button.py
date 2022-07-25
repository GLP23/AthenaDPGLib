# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from dataclasses import dataclass, field, InitVar
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaDearPyGuiLib.models.dpg_component import DpgComponent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class Button(DpgComponent):
    label:str=NOTHING

    # non init

    def __post_init__(self):
        with dpg.stage() as stage:
            self.id = self.dpg_raw()
        self.stage = stage

    def dpg_raw(self):
        return dpg.add_button(
            label=self.label,
            callback=self.callback,
        )

    def callback(self):
        pass

