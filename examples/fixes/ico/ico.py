# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.fixes.taskbar_icon import fix_icon_for_taskbar

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    ICON = "ATHENA.ico"
    TITLE = "IconExample"

    dpg.create_context()
    dpg.create_viewport(title=TITLE, width=600, height=300, large_icon=ICON, small_icon=ICON)
    fix_icon_for_taskbar(TITLE)

    with dpg.window(label="Example of the Icon"):
        dpg.add_text("You should see an icon in your taskbar.\nOnly works for windows currently")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()