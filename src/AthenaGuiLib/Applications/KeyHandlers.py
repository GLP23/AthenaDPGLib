# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from typing import Callable
from functools import partial

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class GlobalKeyHandler:
    def __init__(self):
        self.setup_dictionary = {
            "key_press": {},
            "key_release": {},
            "key_hold": {},
            "key_combo": {}
        }

    def add_key_press(self, key:int, callback:Callable):
        if key in self.setup_dictionary["key_press"]:
            raise KeyError("No Duplicates allowed")
        self.setup_dictionary["key_press"][key] = callback

    def add_key_release(self, key:int, callback:Callable):
        if key in self.setup_dictionary["key_release"]:
            raise KeyError("No Duplicates allowed")
        self.setup_dictionary["key_release"][key] = callback

    def add_key_combination(self, *keys:int, callback:Callable):
        key_start, *key_other = keys
        if key_start not in self.setup_dictionary["key_combo"]:
            self.setup_dictionary["key_combo"][key_start] = {}
        self.setup_dictionary["key_combo"][key_start][tuple(key_other)] = callback

    def _find_key_combo(self, key_start, key_other):
        for key in key_other:
            if dpg.is_key_pressed(key):
                continue
            return
        self.setup_dictionary["key_combo"][key_start][key_other]()

    def assemble(self):
        with dpg.handler_registry():
            for key, callback in self.setup_dictionary["key_press"].items():
                dpg.add_key_press_handler(
                    key=key,
                    callback=callback
                )
            for key, callback in self.setup_dictionary["key_release"].items():
                dpg.add_key_release_handler(
                    key=key,
                    callback=callback
                )
            for key_start, combo in self.setup_dictionary["key_combo"].items():
                for key_other in combo:
                    dpg.add_key_down_handler(
                        key=key_start,
                        # callback=lambda :print("found")
                        callback=lambda : self._find_key_combo(key_start, key_other)
                    )