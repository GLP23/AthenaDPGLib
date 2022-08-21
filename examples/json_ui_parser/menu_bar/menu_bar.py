# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.functions.json_ui_parser import json_ui_parser

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # example made after the following example:
    #   https://dearpygui.readthedocs.io/en/latest/documentation/menus.html

    # ALWAYS make sure this function is ran beforehand
    dpg.create_context()

    # run the ui parser
    json_ui_parser(
        filepath="menu_bar.json"
    )

    # TODO Register callbacks

    # execute dpg as normally
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()