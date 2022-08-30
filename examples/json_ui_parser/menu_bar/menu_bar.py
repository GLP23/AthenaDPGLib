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
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def print_me(sender, **_):
    print(f"Menu Item: {sender}")

def main():
    # example made after the following example:
    #   https://dearpygui.readthedocs.io/en/latest/documentation/menus.html

    # ALWAYS make sure this function is ran beforehand
    dpg.create_context()

    # run the ui parser
    json_ui_parser(
        filepath="menu_bar.json"
    )

    # TODO Automatically Register callbacks (see old system)
    for item in ["FileSave","FileSaveAs","Settings1","Settings2","Help","WidgetCheckbox","WidgetButton","WidgetColor"]:
        dpg.set_item_callback(item=item, callback=print_me)

    # execute dpg as normally
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()