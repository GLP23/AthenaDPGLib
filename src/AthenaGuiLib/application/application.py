# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library
from AthenaGuiLib.models import (AppInfo, AppSettings)
from AthenaGuiLib.models.Exceptions import ViewportNotSetupException

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Application:
    """
    Class to house all logic and data behind an application

    Order of calls:
        .viewport_define()

        .launch()

    """
    # Keyword arguments on init
    info: AppInfo = field(default_factory=AppInfo.factory)  # All info data is frozen across the instance of an application
    settings: AppSettings = field(default_factory=AppSettings.factory) # All settings can be changed while the application is running

    # class attributes not to be setup on init
    _viewport_setup:bool = field(init=False, default=False)

    # ------------------------------------------------------------------------------------------------------------------
    # - Propeties -
    # ------------------------------------------------------------------------------------------------------------------


    # ------------------------------------------------------------------------------------------------------------------
    # - Viewport related settings -
    # ------------------------------------------------------------------------------------------------------------------
    def viewport_define(self) -> Application:
        dpg.create_viewport(
            title=self.info.name,
            small_icon=self.info.icon_path if self.info.icon_path is not None else '',
            large_icon=self.info.icon_path if self.info.icon_path is not None else '',
            # width=None,
            # height=None,
            # x_pos=None,
            # y_pos=None,
            min_width=self.info.min_width,
            max_width=self.info.max_width,
            min_height=self.info.min_height,
            max_height=self.info.max_height,
            resizable=self.info.resizable,
            # vsync=None,
            # always_on_top=None,
            # decorated=None,
            # clear_color=None,
        )

        # once everything has been set up, set the boolean to true, else the .launch() will fail
        self._viewport_setup = True

        # return self to chain methods after eachother
        return self

    # ------------------------------------------------------------------------------------------------------------------
    # - Launch -
    # ------------------------------------------------------------------------------------------------------------------
    def launch(self) -> None:
        # Do some checks that everything is in order
        if not self._viewport_setup:
            raise ViewportNotSetupException

        # set up the basicis of the dpg
        dpg.create_context()
        dpg.setup_dearpygui()

        # Start the actual application
        dpg.start_dearpygui() # blocking
        dpg.destroy_context()

        # Returns None because the following functions of dpg
        #   ( dpg.start_dearpygui() dpg.destroy_context() ) don't return any values,
        #   and can therefor not return any exit codes
        return

