# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaDearPyGuiLib.models.dpg_component import DpgComponent

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class Window(DpgComponent):
    label:str=NOTHING

    # non init
    children:list = field(init=False, default_factory=list)

    def __post_init__(self):
        with dpg.stage() as stage:
            self.id = dpg.add_window(label=self.label, tag=self.label)
        self.stage = stage

    def add_child(self, child:DpgComponent):
        dpg.move_item(
            child.id,
            parent=self.id
        )
        self.children.append(child)

