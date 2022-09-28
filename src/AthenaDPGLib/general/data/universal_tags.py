# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from enum import Enum

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - LandplotDesigner components -
# ----------------------------------------------------------------------------------------------------------------------
class UniversalTags(str, Enum):
    # Thanks to TwidiAngel for showing me (str, Enum) possibility

    TA = "TA_PrimaryWindow"
    TA_texture_registry = "TA_texture_registry"
    TA_img_icon = "TA_img_icon"
    TA_img_title = "TA_img_title"
