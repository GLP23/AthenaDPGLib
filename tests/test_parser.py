# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import unittest

# Custom Library
from AthenaDPGLib.models.parser.runtimeparser import RuntimeParser

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

def callback_test(sender, app_data, user_data):
    dpg.set_value("text1",user_data)


class TestParser(unittest.TestCase):
    def test_general(self):
        dpg.create_context()
        dpg.create_viewport(title='test General', width=600, height=300)

        filepath = "data/test_single1.xml"
        RuntimeParser(
            filepath,
            callbacks={"btn_1":callback_test}
        ).parse()

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
