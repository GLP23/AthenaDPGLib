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

    @CustomCallbacks.callback(items=["wnd_extra", "open_me"])
    def create_window(self, user_data, **_):
        self.app.parser.parse_file(filepath=user_data)
        # force all callbacks to be set again
        #   (Maybe this isn't the best course of action)
        self.app.callbacks.apply_callbacks()

    @CustomCallbacks.on_close(items=["special_window_1","special_window_2"])
    def on_window_close(self, sender, **_):
        # aliases have to be cleaned up, else DPG gets mad
        cleanup_aliases((
            sender,
            *(  # Get all child aliases
                dpg.get_item_alias(child)
                for child in dpg.get_item_children(sender)[1]
            )
        ))

@dataclass(slots=True, kw_only=True)
class App(AthenaApplication):
    parser:SubSystem_JsonUiParser = field(init=False)
    callbacks:SubSystem_CustomCallbacks = field(init=False)

    def __post_init__(self):
        self.parser = self.sub_systems_register(
            constructor=lambda app : SubSystem_JsonUiParser(
                app=app,
                gui_folder="gui/",
                excluded_files={"gui/extra_window_1.json","gui/extra_window_2.json"}
            )
        )
        self.callbacks = self.sub_systems_register(
            constructor=lambda app: SubSystem_CustomCallbacks(
                app=app,
            )
        )

if __name__ == '__main__':
    App().run()