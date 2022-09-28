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

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class TA_Viewport(CustomDPGComponent):
    icon:PATHLIKE

    # non init
    vp:str|int = field(init=False)

    @contextmanager
    def dpg(self):
        dpg.create_viewport(
            title='TrackAttack',
            small_icon=self.icon,
            large_icon=self.icon,
            decorated=Core.settings.show_viewport_titlebar
        )
        fix_icon_for_taskbar(app_model_id="TrackAttack")

        yield

