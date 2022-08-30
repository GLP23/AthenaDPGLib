# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import ClassVar, Callable

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomDPGItems:
    items:ClassVar[dict[str:Callable]] = {}
    items_context_managed:ClassVar[dict[str:Callable]] = {}
    # ------------------------------------------------------------------------------------------------------------------
    # - Decorators -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def custom_dpg_item(cls, fnc:Callable):
        cls._check_fnc_name(fnc_name := fnc.__name__)
        cls.items[fnc_name] = fnc
        return fnc

    @classmethod
    def custom_dpg_item_context_managed(cls, fnc:Callable):
        cls._check_fnc_name(fnc_name := fnc.__name__)
        cls.items_context_managed[fnc_name] = fnc
        return fnc

    # ------------------------------------------------------------------------------------------------------------------
    # - FIXES -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def _check_fnc_name(cls, fnc_name:str):
        if fnc_name in cls.items_context_managed or fnc_name in cls.items:
            raise ValueError

