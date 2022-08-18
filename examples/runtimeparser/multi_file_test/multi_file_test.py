# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.models.application import Application
from AthenaDPGLib.models.runtimeparser.parser_runtime import ParserRuntime
from AthenaDPGLib.models.callbacks import Callbacks

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
app: Application

class CustomCallbacks(Callbacks):
    @Callbacks.callback(items=["create_window"])
    def create_window(self,**_):
        global app
        app.parser.parse_file("extra_window.json")

def main():
    global app
    app = Application(
        name="Multi File Test",
        callbacks=CustomCallbacks(),
    )
    app.parser.parse_file("multi_file_test.json")
    app.main()

if __name__ == '__main__':
    main()
