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