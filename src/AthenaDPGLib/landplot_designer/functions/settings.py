# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import json

# Custom Library
from AthenaLib.constants.types import PATHLIKE

# Custom Packages
from AthenaDPGLib.general.data.universal_tags import LandplotSettings

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def retrieve_settings(filepath: PATHLIKE):
    # Open the file to retrieve the stored settings
    with open(filepath, "r") as file:
        settings = json.load(file)

    # Apply the settings as a value registry for DPG
    #   This allows for easy tie-ins of setting buttons, etc..
    dpg.set_value(LandplotSettings.plot_show_chunks, settings["ui"]["plot"]["show_chunks"])
    dpg.set_value(LandplotSettings.plot_show_polygons, settings["ui"]["plot"]["show_polygons"])
    dpg.set_value(LandplotSettings.plot_show_origins, settings["ui"]["plot"]["show_origins"])


# ----------------------------------------------------------------------------------------------------------------------
def output_settings(filepath: PATHLIKE):
    # Construct the dictionary
    settings_dict = {
        "ui": {
            "plot": {
                "show_chunks": dpg.get_value(LandplotSettings.plot_show_chunks),
                "show_polygons": dpg.get_value(LandplotSettings.plot_show_polygons),
                "show_origins": dpg.get_value(LandplotSettings.plot_show_origins),
            }
        }
    }
    # Write the dictionary to the file
    with open(filepath, "w") as file:
        json.dump(obj=settings_dict, fp=file, indent=2)
