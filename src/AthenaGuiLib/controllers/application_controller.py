# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass

# Custom Library
from AthenaGuiLib.entities.application import Application
from AthenaGuiLib.models.appstyle import AppStyle

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    eq=False,
    kw_only=True,
    slots=True
)
class ApplicationController:
    app: Application

    def __post_init__(self):
        # set up the basicis of the dpg, else nothing is going to work while we set up the application
        dpg.create_context()

    def set_background_color(self, style:AppStyle):
        # noinspection PyTypeChecker
        dpg.set_viewport_clear_color(style.viewport_background.export())

    # ------------------------------------------------------------------------------------------------------------------
    # - Launch and quit of the program-
    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        """
        Defines a loop, which in most cases will only run once, but allows for a restart of the application
        """
        while True:
            self.launch()
            self.quit()
            if self.app.restart:
                continue
            break
            # else, the restart option is set, and this will allow for a new application startup

    @staticmethod
    def quit() -> bool:
        dpg.destroy_context()
        return False # if true, this will enact a restart

    def launch(self) -> None:
        self.app.viewport_define()

        dpg.setup_dearpygui()

        dpg.show_viewport()

        dpg.start_dearpygui()  # blocking


        # Returns None because the following functions of dpg
        #   ( dpg.start_dearpygui() dpg.destroy_context() ) don't return any values,
        #   and can therefor not return any exit codes
        #   the Exit code is handled by self.quit()
        return