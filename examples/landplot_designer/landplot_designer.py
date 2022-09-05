# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.landplot_designer.functions.landplot_constructor import landplot_constructor
import AthenaDPGLib.landplot_designer.data.memory as Memory

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    dpg.create_context()
    dpg.create_viewport(title='Landplot designer Example')

    landplot_constructor()

    dpg.set_primary_window(Memory.landplot_designer.window_tag, True)

    dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()