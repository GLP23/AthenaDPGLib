# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.json_ui_parser.functions.json_ui_parser import json_ui_parser

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # example made after the following example:
    #   https://dearpygui.readthedocs.io/en/latest/documentation/drawing-api.html

    # ALWAYS make sure this function is ran beforehand
    dpg.create_context()

    # run the ui parser
    json_ui_parser(
        filepath="drawing_api.json"
    )

    # execute dpg as normally
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()