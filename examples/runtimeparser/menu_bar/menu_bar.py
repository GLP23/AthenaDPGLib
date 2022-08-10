# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.models.parser.runtimeparser import RuntimeParser, Callbacks

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomCallbacks(Callbacks):
    @staticmethod
    def print_me(sender):
        print(f"Menu Item: {sender}")

def main():
    dpg.create_context()
    RuntimeParser(
        "menu_bar.xml",
        callbacks=CustomCallbacks()
    ).parse()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
