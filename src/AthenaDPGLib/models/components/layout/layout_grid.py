# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages
from AthenaDPGLib.models.dpg_component import DpgComponent
from AthenaDPGLib.models.components.basic.button import Button

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class LayoutGrid(DpgComponent):
    items:list[list[DpgComponent]]=field(default_factory=list)
    horizontal:bool=False

    # non init
    children:list = field(init=False, default_factory=list)

    def __post_init__(self):
        with dpg.stage() as stage:
            with dpg.table(header_row=False) as table:
                self.id = table

                for _ in self.items:
                    dpg.add_table_column()

                for col in self.items:
                    with dpg.table_row() as row:
                        for item in col:
                            if item is None:
                                dpg.add_text("NONE")
                                continue
                            dpg.move_item(item.id, parent=row)
                            dpg.unstage(item.stage)

        self.stage = stage