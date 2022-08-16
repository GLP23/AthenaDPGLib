# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.models.runtimeparser.parser_runtime import ParserRuntime, Callbacks

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
parser: ParserRuntime

class CustomCallbacks(Callbacks):
    @Callbacks.callback
    def print_me(self, sender):
        print(f"Menu Item: {sender}")
    @Callbacks.callback
    def create_window(self):
        global parser
        parser.parse_file("extra_window.json")

def main():
    dpg.create_context()
    global parser
    parser = ParserRuntime(callbacks=CustomCallbacks())
    parser.parse_file("multi_file_test.json")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
