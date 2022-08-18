# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaDPGLib.models.application import Application
from AthenaDPGLib.models.callbacks import Callbacks

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomCallbacks(Callbacks):
    @Callbacks.callback(
        items=["FileSave","FileSaveAs","Settings1","Settings2","Help","WidgetCheckbox","WidgetButton","WidgetColor"]
    )
    def print_me(self,sender, **_):
        print(f"Menu Item: {sender}")

def main():
    app = Application(
        name="Menubar Example",
        gui_folder="../menu_bar",
        callbacks=CustomCallbacks()
    )
    app.main()

if __name__ == '__main__':
    main()
