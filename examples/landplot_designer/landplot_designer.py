# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.landplot_designer.models.core import Core
from AthenaDPGLib.landplot_designer.main import main as landplot_designer_main

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

def main():
    dpg.create_context()
    dpg.create_viewport(title='Landplot designer Example')

    landplot_designer_main()

    dpg.set_primary_window(Core.designer_plot.window_tag, True)

    dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()