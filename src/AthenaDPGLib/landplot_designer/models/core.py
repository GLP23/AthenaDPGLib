# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import ClassVar, Any
# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Core:
    chunk_manager: ClassVar[Any]
    designer_plot: ClassVar[Any]
    designer_plot_debug: ClassVar[Any]

    __slots__ = [
        "chunk_manager",
        "designer_plot",
        "designer_plot_debug"
    ]
