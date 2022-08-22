# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
# Custom Library

# Custom Packages
from AthenaDPGLib.models.athena_application.athena_application import AthenaApplication
from AthenaDPGLib.models.athena_application.sub_systems.json_ui_parser import JsonUiParser

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class App(AthenaApplication):
    def __post_init__(self):
        self.sub_systems_register(
            constructor=lambda app : JsonUiParser(
                app=app,
                gui_folder="gui/"
            )
        )

if __name__ == '__main__':
    app = App()
    app.run()