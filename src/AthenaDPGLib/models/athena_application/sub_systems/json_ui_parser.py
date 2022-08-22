# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.functions.files import gather_all_filepaths

# Custom Packages
from AthenaDPGLib.models.athena_application.athena_application import SubSystem
from AthenaDPGLib.models.json_ui_parser.custom_dpg_items_premade import CustomDPGItems_PreMade
from AthenaDPGLib.functions.json_ui_parser import json_ui_parser

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class JsonUiParser(SubSystem):
    """
    Sub System which has to be run after the DPG context has been generated
    This Sub System handles JSON as dpg ui files parsing
    """
    gui_folder:str
    custom_dpg_items:CustomDPGItems_PreMade = field(default_factory=CustomDPGItems_PreMade)
    tags:set = field(default_factory=set)

    def __post_init__(self):
        for filepath in gather_all_filepaths(directory=self.gui_folder, extensions={"json"}):
            json_ui_parser(
                filepath,
                custom_dpg_items=self.custom_dpg_items,
                tags=self.tags
            )
