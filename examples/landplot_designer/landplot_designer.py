# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaDPGLib.landplot_designer.models.core import Core
from AthenaDPGLib.landplot_designer.main import main as landplot_designer_main
from AthenaDPGLib.landplot_designer.functions.settings import output_settings

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

def main():
    dpg.create_context()
    dpg.create_viewport(title='Landplot designer Example')

    landplot_designer_main(
        settings_filepath="settings.json"
    )

    dpg.set_primary_window(Core.designer_plot.window_tag, True)

    dpg.show_metrics()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui() # blocking call
    output_settings(
        filepath="settings.json"
    )
    dpg.destroy_context()


if __name__ == '__main__':
    main()