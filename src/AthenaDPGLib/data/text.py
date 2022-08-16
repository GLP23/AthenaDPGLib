# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

# Strings that are often reused within the library
#   Stored here to be created once, and then just referenced afterwards
TAG:str = "tag"
CALLBACK:str = "callback"
DRAG_CALLBACK:str = "drag_callback"
DROP_CALLBACK:str = "drop_callback"
PRIMARY_WINDOW:str = "primary_window"
POLICY:str = "policy"

# Sets that are often reused within the library
SKIP_ATTRIB:set[str] = {"_children", CALLBACK, DRAG_CALLBACK, DROP_CALLBACK}
SKIP_ATTRIB_GRID_LAYOUT:set[str] = {"_columns", "_rows","_children","_row_all"}