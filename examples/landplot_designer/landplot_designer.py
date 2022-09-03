# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.landplot_designer.ui.landplot_designer import LandplotDesigner

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    dpg.create_context()
    dpg.create_viewport(title='Landplot designer Example')

    landplot_designer = LandplotDesigner()
    landplot_designer.add_dpg()
    # with landplot_designer.dpg():
    #     pass

    dpg.set_primary_window(landplot_designer.window_tag, True)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()