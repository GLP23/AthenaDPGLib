# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaDPGLib.models.landplot_designer.memory import LandplotDesignerMemory

from AthenaDPGLib.data.landplot import landplot_designer_memory

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class LandplotDesigner_Component():
    # non init
    memory:LandplotDesignerMemory = field(init=False, default=landplot_designer_memory)