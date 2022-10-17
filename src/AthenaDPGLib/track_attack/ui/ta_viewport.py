# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from contextlib import contextmanager
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.constants.types import PATHLIKE

# Custom Packages
from AthenaDPGLib.general.ui.custom_dpg_component import CustomDPGComponent
from AthenaDPGLib.fixes.taskbar_icon import fix_icon_for_taskbar
from AthenaDPGLib.track_attack.models.core import Core
from AthenaDPGLib.track_attack.models.settings import SettingsEnum
from AthenaDPGLib.track_attack.models.settings.hooks import HasSettingsHooks
from AthenaDPGLib.track_attack.functions.decorations import register_settings_hook

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class TA_Viewport(CustomDPGComponent, HasSettingsHooks):
    icon:PATHLIKE

    # non init
    vp:str|int = field(init=False)

    @contextmanager
    def dpg(self):
        dpg.create_viewport(
            title='TrackAttack',
            small_icon=self.icon,
            large_icon=self.icon,
            decorated=Core.settings.viewport_show_title,
            x_pos=Core.settings.viewport_x,
            y_pos=Core.settings.viewport_y,
            width=Core.settings.viewport_width,
            height=Core.settings.viewport_height,
            vsync=Core.settings.viewport_vsync,
        )
        fix_icon_for_taskbar(app_model_id="TrackAttack")

        # Add certain other systems to it
        dpg.set_viewport_resize_callback(
            callback=self.store_pos_and_size
        )

        # More settings that adhere to something
        if Core.settings.viewport_fullscreen:
            dpg.toggle_viewport_fullscreen()
        if Core.settings.debug_show:
            self.debug_show()
        if Core.settings.metrics_show:
            self.metrics_show()

        yield

    @register_settings_hook(SettingsEnum.viewport_show_title)
    def switch_title_visibility(self):
        dpg.set_viewport_decorated(Core.settings.viewport_show_title)

    def store_pos_and_size(self):
        x,y = dpg.get_viewport_pos()
        Core.settings.viewport_x = x
        Core.settings.viewport_y = y
        Core.settings.viewport_width = dpg.get_viewport_width()
        Core.settings.viewport_height = dpg.get_viewport_height()


    @register_settings_hook(SettingsEnum.debug_show)
    def debug_show(self):
        dpg.show_debug()

    @register_settings_hook(SettingsEnum.metrics_show)
    def metrics_show(self):
        dpg.show_metrics()

