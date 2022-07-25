# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from dataclasses import dataclass, field
from typing import Any
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class DpgComponent:
    id:str = field(init=False)
    stage:Any = field(init=False)

    min_width:int=0
    max_width:int=0
    min_height:int=0
    max_height:int=0

    def constrain(self):
        if not any((self.min_width,self.max_width,self.min_height,self.max_height)):
            return

        # height = dpg.get_item_height(self.id)
        width = dpg.get_item_width(self.id)

        if self.max_width:
            width = min(self.max_width , width)
        if self.min_width:
            width = max(self.min_width , width)
        # if self.max_height:
        #     height = min(self.max_height , height)
        # if self.min_height:
        #     height = max(self.min_height , height)

        # if height is not None:
        #     dpg.set_item_height(self.id, height)
        dpg.set_item_width(self.id, width)