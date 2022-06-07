# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library

# Custom Packages
from AthenaGuiLib.Applications.ApplicationInfo import AppInfo

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Application:
    # Keyword arguments on init
    app_info_path:str
    _force_app_info:bool=False

    # Internal stuff
    info:AppInfo=field(init=False)

    # ------------------------------------------------------------------------------------------------------------------
    # - Class Init -
    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        # Makes sure some app information is set up, if the setting is enabled.
        #   A force to generate new app info is intyegerated to easily create new applications in tests
        try:
            app_info = AppInfo(path=self.app_info_path)
        except FileNotFoundError :
            if not self._force_app_info:
                raise
            app_info = AppInfo(_empty=True)
        self.info = app_info

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
        dpg.start_dearpygui()
        dpg.destroy_context()