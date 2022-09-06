# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.general.data.universal_tags import LandplotSettings,LandplotDebug

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def populate_value_registry():
    with dpg.value_registry(tag=LandplotSettings.settings_registry):
        # Settings values
        dpg.add_bool_value(tag=LandplotSettings.plot_show_chunks)
        dpg.add_bool_value(tag=LandplotSettings.plot_show_polygons)
        dpg.add_bool_value(tag=LandplotSettings.plot_show_origins)

        # Plot Debug values
        dpg.add_string_value(tag=LandplotDebug.shown_chunks)
        dpg.add_string_value(tag=LandplotDebug.shown_polygons)
        dpg.add_string_value(tag=LandplotDebug.plot_offset)
        dpg.add_string_value(tag=LandplotDebug.plot_scale)
        dpg.add_string_value(tag=LandplotDebug.plot_limit_min)
        dpg.add_string_value(tag=LandplotDebug.plot_limit_max)
