# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field
import ctypes
import sys
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.models import Version

# Custom Packages
from AthenaGuiLib.viewports import Viewport

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    slots=True,
    kw_only=True # done to make sure the programmer knows what the hell they are doing
)
class Application:
    title:str="UNDEFINED"
    version:Version=field(default_factory=lambda:Version(0,"PreAlpha",0))
    icon_path:str=None
    icon_enabled:bool=True
    viewports:set[Viewport,...]=field(default_factory=set)

    # post init stuff
    model_id:str=field(init=False)

    # ------------------------------------------------------------------------------------------------------------------
    # - Init stuff-
    # ------------------------------------------------------------------------------------------------------------------
    def __post_init__(self):
        self.model_id = f"{self.title}[{self.version.to_str(sep='.')}]"

    # ------------------------------------------------------------------------------------------------------------------
    # - Viewport stuff -
    # ------------------------------------------------------------------------------------------------------------------
    def get_viewport(self) -> Viewport:
        # if no viewport has been defined yet, you need to make one
        #   Else dpg will fail
        if not self.viewports:
            viewport = Viewport()
            self.viewports.add(viewport)
        else:
            # currently in dpg there is only one viewport available, but this will change in later versions
            viewport, = self.viewports
        return viewport

    # ------------------------------------------------------------------------------------------------------------------
    # - Fixes -
    # ------------------------------------------------------------------------------------------------------------------
    def fix_icon_for_taskbar(self):
        # retrieve the viewport object, if it hasn't been done before, it'll set up a new one
        viewport:Viewport = self.get_viewport()

        # Define application ICON,
        #   makes sure the APPLICATION icon is shown in the taskbar
        if sys.platform == "win32":
            # WINDOWS NEEDS THIS to make this possible
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                self.model_id
            )
        else:
            # TODO fix this! (aka, find out how to do this)
            raise NotImplementedError

        # actually set the icon
        viewport.set_icon(icon_path=self.icon_path)