# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable, ClassVar
from dataclasses import dataclass

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class _Parser:
    custom_dpg:ClassVar[dict[str:Callable]]={}

    @classmethod
    def custom_dpg_item(cls,fnc):
        cls.custom_dpg[fnc.__name__] = fnc
        return fnc