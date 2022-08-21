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
# use a globally set tags object to make sure the second json parser doesn't create duplicate tags
tags = set()

def create_window_callback():
    # This allows for a file to be edited after it has been parsed.
    # When the file is called again, the resulting window can change
    # Allowing for files to be created at run time and then read
    global tags
    json_ui_parser(
        filepath="extra_window.json",
        tags = tags
    )


def main():
    # Custom-made example

    # ALWAYS make sure this function is ran beforehand
    dpg.create_context()

    # run the ui parser
    global tags
    json_ui_parser(
        filepath="multi_file_test.json",
        tags = tags
    )

    # TODO Automatically register callbacks
    dpg.set_item_callback(
        item="create_window",
        callback=create_window_callback
    )

    # execute dpg as normally
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()