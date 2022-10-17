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
    """
    Enum class that stores all string values of used tags as AthenaDPGLib's DPG items.
    This is meant to cause as little duplicate usages of tags as possible throughout my libraries.
    """
    # Thanks to TwidiAngel for showing me (str, Enum) possibility

    TA = "TA_PrimaryWindow"
    TA_texture_registry = "TA_texture_registry"
    TA_shortcut_registry = "TA_shortcut_registry"
    TA_img_icon = "TA_img_icon"
    TA_img_title = "TA_img_title"
