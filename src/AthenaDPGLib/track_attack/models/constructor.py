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

from AthenaDPGLib.track_attack.data.res import images

from AthenaDPGLib.track_attack.models.core import Core
from AthenaDPGLib.track_attack.models.texture_registry import TextureRegistry
from AthenaDPGLib.track_attack.models.data_tracker import DataTracker
from AthenaDPGLib.track_attack.ui.track_attack import TrackAttack
from AthenaDPGLib.track_attack.ui.ta_viewport import TA_Viewport

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Constructor(AbstractConstructor):
    @staticmethod
    def _data():
        Core.texture_registry = TextureRegistry()
        for path, tag in images:
            Core.texture_registry.load_image(path, tag)

    @staticmethod
    def _functionality():
        Core.data_tracker = DataTracker(db="project_tracking.db")

    @staticmethod
    def _ui():
        # setup viewport
        Core.ui_viewport = TA_Viewport(icon="res/TrackAttack.ico")
        Core.ui_viewport.add_dpg()
        dpg.setup_dearpygui()

        # setup ui items
        Core.ui_track_attack = TrackAttack(primary_window_tag=UniversalTags.TA)
        Core.ui_track_attack.add_dpg()

        dpg.show_viewport()
        dpg.set_primary_window(UniversalTags.TA, True)

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