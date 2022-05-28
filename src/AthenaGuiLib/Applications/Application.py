# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import ctypes
from dataclasses import dataclass, field
import sys
from typing import Any

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

    _icon_small:str=field(init=False, repr=False)
    _icon_large:str=field(init=False, repr=False)

    context:Any = field(init=False)
    viewport:Any = field(init=False)

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

    # ------------------------------------------------------------------------------------------------------------------
    # - Propeties -
    # ------------------------------------------------------------------------------------------------------------------


    # ------------------------------------------------------------------------------------------------------------------
    # - DearPyGui stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def launch(self):

        dpg.create_context()
        dpg.create_viewport()
        dpg.create_viewport()
        dpg.setup_dearpygui()

        # Define application ICON,
        #   makes sure the application icon is shown in the taskbar
        if sys.platform == "win32":  # WINDODWS NEEDS THIS to make this possible
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"{self.info.name}[{self.info.version}]")
        elif sys.platform in ("linux", "linux2"):
            raise NotImplementedError #TODO fix this!

        dpg.set_viewport_small_icon(self.info.icon)
        dpg.set_viewport_large_icon(self.info.icon)

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()