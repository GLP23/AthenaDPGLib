# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library
from AthenaGuiLib.entities.style.style_sheet import StyleSheet

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    eq=False, # no need for equal check
    kw_only=True,
    slots=True
)
class StyleLibrary:
    styles:dict[str:StyleSheet] = field(default_factory=dict)