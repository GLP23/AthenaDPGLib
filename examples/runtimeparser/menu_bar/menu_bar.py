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
class CustomCallbacks(Callbacks):
    @Callbacks.callback
    def print_me(self,sender):
        print(f"Menu Item: {sender}")

def main():
    dpg.create_context()
    ParserRuntime(
        callbacks=CustomCallbacks()
    ).parse_file("menu_bar.json")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
