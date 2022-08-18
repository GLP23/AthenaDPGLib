# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library
from AthenaDPGLib.models.application import Application

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    app = Application(
        name="Drawing API Example",
        gui_folder="../drawing_api"
    )
    app.main()

if __name__ == '__main__':
    main()
