# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # Created a second version of the test, according to the original solution Hoffstadt posted
    # https://github.com/hoffstadt/DearPyGui/issues/1024#issuecomment-875163747
    ICON = "ATHENA.ico"
    TITLE = "IconExample"

    dpg.create_context()
    vp = dpg.create_viewport(title=TITLE, width=600, height=300)
    dpg.setup_dearpygui(viewport=vp)

    dpg.set_viewport_small_icon(ICON)
    dpg.set_viewport_large_icon(ICON)

    # indeed excluding the following line works to actually show the icon in the taskbar
    #   But by all accords, we are seemingly doing the same, except for a very strange order
    # fix_icon_for_taskbar(TITLE)

    dpg.show_viewport()

    with dpg.window(label="Example of the Icon"):
        dpg.add_text("You should see an icon in your taskbar.\nOnly works for windows currently")

    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()