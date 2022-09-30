# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from contextlib import contextmanager
from dataclasses import dataclass

# Custom Library

# Custom Packages
from AthenaDPGLib.general.ui.custom_dpg_component import CustomDPGComponent
from AthenaDPGLib.track_attack.models.core import Core
from AthenaDPGLib.general.data.universal_tags import UniversalTags

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True)
class TrackAttack(CustomDPGComponent):
    """
    Credits:
        Name of 'Track Attack' by Wh4i3
    """
    primary_window_tag:str

    @contextmanager
    def dpg(self):
        with dpg.window(tag=self.primary_window_tag) as window:
            dpg.add_image(UniversalTags.TA_img_title, width=100, height=int(100/(32.24/15.61)))
            yield window

