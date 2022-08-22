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
error_tag = lambda tag, item : ValueError(
    f"'{tag}' was already present in the tags set.\nRaised in '{item}' item"
)
error_item = lambda item : ValueError(
    f"'{item}' dpg item name could not be parsed as a default dpg item or a custom item"
)
error_file = lambda filepath : ValueError(
    f"The file `{filepath}` had no usable structure"
)