# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.models.application import Application
from AthenaDPGLib.models.runtimeparser.parser_runtime import ParserRuntime
from AthenaDPGLib.models.callbacks import Callbacks

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
parser: ParserRuntime

class CustomCallbacks(Callbacks):
    @Callbacks.callback(items=["create_window"])
    def create_window(self):
        global parser
        parser.parse_file("extra_window.json")

def main():
    app = Application(
        name="Multi File Test",
        callbacks=CustomCallbacks(),
        gui_folder="../multi_file_test",
        translations_enabled=False
    )

    dpg.create_context()
    global parser
    parser = ParserRuntime()
    parser.parse_file("multi_file_test.json")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
