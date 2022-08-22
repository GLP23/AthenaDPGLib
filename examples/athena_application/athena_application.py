# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.models.athena_application.athena_application import AthenaApplication
from AthenaDPGLib.models.athena_application.sub_systems.json_ui_parser import SubSystem_JsonUiParser
from AthenaDPGLib.models.athena_application.sub_systems.custom_callbacks import SubSystem_CustomCallbacks
from AthenaDPGLib.models.custom_callbacks import CustomCallbacks
from AthenaDPGLib.functions.cleanups import cleanup_aliases

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class AppExample_CustomCallbacks(SubSystem_CustomCallbacks):
    app:App

    @staticmethod
    @CustomCallbacks.callback(items=["wnd_extra", "close_me"])
    def print_me(sender,**_):
        print(f"Menu Item: {sender}")

    @CustomCallbacks.callback(items=["wnd_extra"])
    def create_window(self, **_):
        dpg.hide_item("wnd_extra")
        self.app.parser.parse_file(filepath="gui/extra_window.json")
        self.app.callbacks.apply_callbacks_specific(items={"wnd_extra","special_window","close_me"})

    @CustomCallbacks.on_close(items=["special_window"])
    def create_window_close(self, **_):
        dpg.show_item("wnd_extra")

        cleanup_aliases(("special_window", "close_me"))

@dataclass(slots=True, kw_only=True)
class App(AthenaApplication):
    parser:SubSystem_JsonUiParser = field(init=False)
    callbacks:SubSystem_CustomCallbacks = field(init=False)

    def __post_init__(self):
        self.parser = self.sub_systems_register(
            constructor=lambda app : SubSystem_JsonUiParser(
                app=app,
                gui_folder="gui/",
                excluded_files={"gui/extra_window.json"}
            )
        )
        self.callbacks = self.sub_systems_register(
            constructor=lambda app: SubSystem_CustomCallbacks(
                app=app,
            )
        )

if __name__ == '__main__':
    App().run()