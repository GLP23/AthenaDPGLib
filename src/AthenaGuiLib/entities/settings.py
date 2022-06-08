# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    eq=False, # no need for equal check
    kw_only=True,
    slots=True
)
class Settings:
    """
    Application Settings class, houses all the changable information of an application
    Aka: fullscreen state, position, etc
    """
    pass