# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.functions.files import gather_all_filepaths

# Custom Packages
from AthenaDPGLib.models.component import Component
from AthenaDPGLib.models.components.ui_parser.ui_parser import UIParser
from AthenaDPGLib.data.sets import UI_EXTENSIONS

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class ComponentUIParser(Component):

    # non init
    tags: ClassVar[set] = set()
    parser: UIParser = field(init=False)

    def component_startup(self, *args, **kwargs):
        self.parser = UIParser()

    def parse_gui_files(self, gui_folder):
        for filepath in gather_all_filepaths(gui_folder, extensions=UI_EXTENSIONS):
            self.parser.parse_file(filepath)