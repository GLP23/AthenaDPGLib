# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import Callable
from dataclasses import dataclass,field
import functools

# Custom Library
from AthenaLib.functions.files import gather_all_filepaths


# Custom Packages
from AthenaDPGLib.functions.fixes import fix_icon_for_taskbar
from AthenaDPGLib.models.runtimeparser.parser_runtime import ParserRuntime
from AthenaDPGLib.models.callbacks import Callbacks
from AthenaDPGLib.models.translation.translation import Translation
from AthenaDPGLib.models.translation.languages import Languages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Application:
    name:str
    gui_folder:str|None = None
    callbacks:Callbacks = field(default_factory=Callbacks)
    translations:Translation = field(default_factory=Translation)

    # non init
    viewport_resize_callbacks:list[Callable] = field(init=False,default_factory=list)
    parser:ParserRuntime = field(init=False,default_factory=ParserRuntime)

    def create_viewport(self):
        dpg.create_viewport(title=self.name)

    def parse_gui_files(self):
        if self.gui_folder is not None:
            for filepath in gather_all_filepaths(self.gui_folder):
                self.parser.parse_single_file(filepath)

    def parse_translation(self, language:Languages):
        self.translations.connect()
        self.translations.apply_translation(language=language)

    def parse_callbacks(self):
        for tag in self.callbacks.mapping_callback:
            dpg.set_item_callback(item=tag, callback=self.callbacks.chain_callback)
        for tag in self.callbacks.mapping_drag_callback:
            dpg.set_item_callback(item=tag, callback=self.callbacks.chain_drag_callback)
        for tag in self.callbacks.mapping_drop_callback:
            dpg.set_item_callback(item=tag, callback=self.callbacks.chain_drop_callback)

        dpg.set_viewport_resize_callback(callback=self.callbacks.chain_viewport_resize)


    def main(self):
        dpg.create_context()
        self.create_viewport()

        self.parse_gui_files()
        self.parse_callbacks()
        self.parse_translation(language=Languages.english)

        fix_icon_for_taskbar(app_model_id=self.name)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def register_viewport_resize_callback(self, fnc:Callable):
        self.viewport_resize_callbacks.append(fnc)

