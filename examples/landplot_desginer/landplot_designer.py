# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.models.landplot_designer.landplot_designer import LandplotDesigner

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    dpg.create_context()
    dpg.create_viewport(title='LandPlot Designer Example')

    LandplotDesigner(window_tag="primary_window").constructor()

    dpg.set_primary_window("primary_window", True)

    dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()