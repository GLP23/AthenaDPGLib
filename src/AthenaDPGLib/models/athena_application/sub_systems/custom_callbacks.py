# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.models.athena_application.athena_application import SubSystem
from AthenaDPGLib.functions.custom_callback import apply_callbacks

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class SubSystem_CustomCallbacks(SubSystem):
    """
    Sub System which has to be run after the DPG context has been generated
        and after any GUI elements have been generated
    """

    def __post_init__(self):
        apply_callbacks()