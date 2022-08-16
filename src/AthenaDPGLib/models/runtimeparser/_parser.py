# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import functools
from typing import Callable, ClassVar
from dataclasses import dataclass

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class _Parser:
    """
    Class made do be inherited by the actual ParserRuntime class
    Holds the decorators meant to be used within the ParserRuntime to assign custom dpg items
    """
    custom_dpg:ClassVar[dict[str:Callable]]={}

    @classmethod
    def custom_dpg_item(cls,name:str):
        """
        Decorator which assigns the method as a custom dpg item which can be used within the json ui files.
        """
        def decorator(fnc):
            cls.custom_dpg[name] = fnc
        return decorator