# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Callbacks:
    # part of the actual class?
    mapping_callback:dict[str:Callable] = {}
    mapping_drag_callback:dict[str:Callable] = {}
    mapping_drop_callback:dict[str:Callable] = {}
    mapping_on_enter:dict[str:Callable] = {}

    @classmethod
    def callback(cls,fnc:Callable):
        cls.mapping_callback[fnc.__name__] = fnc
        return fnc

    @classmethod
    def drag_callback(cls, fnc:Callable ):
        cls.mapping_drag_callback[fnc.__name__] = fnc
        return fnc

    @classmethod
    def drop_callback(cls, fnc:Callable):
        cls.mapping_drop_callback[fnc.__name__] = fnc
        return fnc

    @classmethod
    def on_enter(cls, fnc:Callable):
        cls.mapping_on_enter[fnc.__name__] = fnc
        return fnc