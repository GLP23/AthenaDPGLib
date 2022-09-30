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
from AthenaDPGLib.general.models.texture_registry import TextureRegistry
from AthenaDPGLib.general.models.shortcut_registry import ShortcutRegistry
from AthenaDPGLib.track_attack.functions.assign_shortcuts import assign_shortcuts

from AthenaDPGLib.track_attack.models.core import Core
from AthenaDPGLib.track_attack.models.data_interaction import DataInteraction
from AthenaDPGLib.track_attack.models.settings import Settings

from AthenaDPGLib.track_attack.ui.track_attack import TrackAttack
from AthenaDPGLib.track_attack.ui.ta_viewport import TA_Viewport

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Constructor(AbstractConstructor):

    @staticmethod
    def _stage0_pre():
        # Create the context to be used within the data and other systems,
        #   as dpg needs this to work properly
        dpg.create_context()

    @staticmethod
    def _stage1_data():
        Core.settings = Settings()
        Core.settings.load_from_file(filepath="config/settings.json")

        # Texture registry:
        #   Loads images into DPG memory
        Core.texture_registry = TextureRegistry(tag=UniversalTags.TA_texture_registry)
        images = [
            ("res/TrackAttack_Icon.png", UniversalTags.TA_img_icon),
            ("res/TrackAttack_Title.png", UniversalTags.TA_img_title)
        ]
        for path, tag in images:
            Core.texture_registry.load_image(path, tag)

    @staticmethod
    def _stage2_functionality():
        Core.data_interaction = DataInteraction(db="project_tracking.db")

    @staticmethod
    def _stage3_ui():
        # setup viewport
        Core.ui_viewport = TA_Viewport(icon="res/TrackAttack.ico")
        Core.ui_viewport.add_dpg()
        dpg.setup_dearpygui()

        # setup ui items
        Core.ui_track_attack = TrackAttack(primary_window_tag=UniversalTags.TA)
        Core.ui_track_attack.add_dpg()

        dpg.show_viewport()
        dpg.set_primary_window(UniversalTags.TA, True)

    @staticmethod
    def _stage4_other():
        # assign shortcuts after every component of the application has been created
        #   this is due to shortcuts need of various ui, data and/or functionality components
        Core.shortcut_registry = ShortcutRegistry(tag=UniversalTags.TA_shortcut_registry)
        assign_shortcuts()

    @staticmethod
    def _stage5_blocking():
        dpg.start_dearpygui()  # blocking call
        Core.threaded_executor.shutdown() # make sure the threaded systems are shut down

    @staticmethod
    def _stage6_shutdown():
        dpg.destroy_context()
        Core.settings.dump_to_file(filepath="config/settings.json")