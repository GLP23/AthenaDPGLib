# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaDPGLib.track_attack.models.core import Core

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def assign_shortcuts():
    # assign key combinations to a callback
    pass

    # At the end: assemble the registry
    Core.shortcut_registry.assemble_registry()