# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import unittest

# Custom Library
from AthenaDPGLib.models.parser.parser import Parser

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

def callback_test(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


class TestParser(unittest.TestCase):
    def test_general(self):
        dpg.create_context()
        dpg.create_viewport(title='test General', width=600, height=300)

        filepath = "data/test_single1.xml"
        Parser(
            filepath,
            callbacks={"btn_1":callback_test}
        ).parse()

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
