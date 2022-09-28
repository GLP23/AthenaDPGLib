# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.general.data.universal_tags import UniversalTags
from AthenaDPGLib.general.models.abstract_constructor import AbstractConstructor

from AthenaDPGLib.track_attack.models.core import Core
from AthenaDPGLib.track_attack.models.data_tracker import DataTracker
from AthenaDPGLib.track_attack.ui.track_attack import TrackAttack

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Constructor(AbstractConstructor):
    @staticmethod
    def _data():
        pass

    @staticmethod
    def _functionality():
        Core.data_tracker = DataTracker(db="project_tracking.db")

    @staticmethod
    def _ui():
        # context( has already been created by the .construct() method
        dpg.create_viewport(title='Project Tracking tool', width=600, height=200)

        Core.ui_track_attack = TrackAttack(
            primary_window_tag=UniversalTags.PTT
        )
        Core.ui_track_attack.add_dpg()

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window(UniversalTags.PTT, True)

        dpg.start_dearpygui()  # blocking call
        Core.threaded_executor.shutdown() # make sure the threaded systems are shut down
        dpg.destroy_context()

    @classmethod
    def construct(cls):
        # Create the context to be used within the data and other systems, 
        #   as dpg needs this to work properly
        dpg.create_context()
        # run as normal
        super(Constructor, cls).construct()