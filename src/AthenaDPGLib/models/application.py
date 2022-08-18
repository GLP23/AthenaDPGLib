# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import Callable
from dataclasses import dataclass,field

# Custom Library
from AthenaLib.functions.files import gather_all_filepaths

# Custom Packages
from AthenaDPGLib.models.cogs.gui_parsing.ui_parser import UIParser
from AthenaDPGLib.models.cogs.callbacks import Callbacks
from AthenaDPGLib.models.cogs.translation.translator import Translator
from AthenaDPGLib.models.cogs.translation.languages import Languages
from AthenaDPGLib.functions.fixes import fix_icon_for_taskbar
import AthenaDPGLib.data.sql as sql_fnc

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Application:
    name:str
    gui_folder:str|None = None
    callbacks:Callbacks = field(default_factory=Callbacks)
    translator:Translator = field(default_factory=Translator)
    translations_enabled:bool = False

    # non init
    viewport_resize_callbacks:list[Callable] = field(init=False,default_factory=list)
    parser:UIParser = field(init=False, default_factory=UIParser)
    viewport_id:str|int|None = field(init=False)

    def __post_init__(self):
        # always makes sure the context exists
        dpg.create_context()

    def create_viewport(self):
        # noinspection PyNoneFunctionAssignment
        self.viewport_id = dpg.create_viewport(title=self.name)

    def parse_gui_files(self):
        if self.gui_folder is not None:
            for filepath in gather_all_filepaths(self.gui_folder, extensions={"json"}):
                self.parser.parse_file(filepath)


    def parse_callbacks(self):
        """
        Goes over all registered callbacks and sets the items' callbacks accordingly
        Will raise errors if the tag doesn't exist yet
        """
        for tag in self.callbacks.mapping_callback:
            dpg.set_item_callback(item=tag, callback=self.callbacks.chain_callback)
        for tag in self.callbacks.mapping_drag_callback:
            dpg.set_item_callback(item=tag, callback=self.callbacks.chain_drag_callback)
        for tag in self.callbacks.mapping_drop_callback:
            dpg.set_item_callback(item=tag, callback=self.callbacks.chain_drop_callback)

        dpg.set_viewport_resize_callback(callback=self.callbacks.chain_viewport_resize)


    def main(self):
        self.create_viewport()

        self.parse_gui_files()
        self.parse_callbacks()
        self.parse_translation(language=Languages.nederlands)

        fix_icon_for_taskbar(app_model_id=self.name)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def register_viewport_resize_callback(self, fnc:Callable):
        self.viewport_resize_callbacks.append(fnc)

