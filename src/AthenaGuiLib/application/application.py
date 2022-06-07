# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library
from AthenaGuiLib.models import AppInfo

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Application:
    # Keyword arguments on init
    info: AppInfo = field(default_factory=AppInfo.factory)

    # Internal stuff

    # ------------------------------------------------------------------------------------------------------------------
    # - Class Init -
    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        # Makes sure some app information is set up, if the setting is enabled.
        #   A force to generate new app info is intyegerated to easily create new applications in tests

        # set up the basicis of the dpg
        dpg.create_context()
        dpg.setup_dearpygui()

    # ------------------------------------------------------------------------------------------------------------------
    # - Propeties -
    # ------------------------------------------------------------------------------------------------------------------


    # ------------------------------------------------------------------------------------------------------------------
    # - DearPyGui stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def launch(self):
        dpg.start_dearpygui() # blocking
        dpg.destroy_context()