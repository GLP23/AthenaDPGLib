# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
# Custom Library

# Custom Packages
from AthenaDPGLib.models.athena_application.athena_application import AthenaApplication
from AthenaDPGLib.models.athena_application.sub_systems.json_ui_parser import SubSystem_JsonUiParser
from AthenaDPGLib.models.athena_application.sub_systems.custom_callbacks import SubSystem_CustomCallbacks
from AthenaDPGLib.models.custom_callbacks import CustomCallbacks

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class AppExample_CustomCallbacks(SubSystem_CustomCallbacks):
    @staticmethod
    @CustomCallbacks.callback(items=["test", "wnd_extra"])
    def print_me(sender,**_):
        print(f"Menu Item: {sender}")

    @staticmethod
    @CustomCallbacks.callback(items=["test", "wnd_extra"])
    def create_window(sender,**_):

        print(f"Menu Item: {sender}")

@dataclass(slots=True, kw_only=True)
class App(AthenaApplication):
    def __post_init__(self):
        self.sub_systems_register(
            constructor=lambda app : SubSystem_JsonUiParser(
                app=app,
                gui_folder="gui/",
                excluded_files={"gui/extra_window.json"}
            )
        )
        self.sub_systems_register(
            constructor=lambda app: SubSystem_CustomCallbacks(
                app=app,
            )
        )

if __name__ == '__main__':
    App().run()