# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import threading
import queue

# Custom Library

# Custom Packages
from AthenaDPGLib.general.data.universal_tags import UniversalTags
from AthenaDPGLib.project_tracking_tool.models.constructor import Constructor
from AthenaDPGLib.general.functions.threaded_executor import get_threaded_executor

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def main():
    dpg.create_context()

    dpg.create_viewport(title='Project Tracking tool', width=600, height=200)

    ptt = Constructor()
    ptt.ui.add_dpg()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(UniversalTags.PTT, True)

    dpg.start_dearpygui() # blocking call
    get_threaded_executor().shutdown()
    dpg.destroy_context()

if __name__ == '__main__':
    main()