# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.track_attack.models.core import Core

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------

def test_shortcut():
    Core.settings.viewport_show_title = not Core.settings.viewport_show_title

def assign_shortcuts():
    # assign key combinations to a callback
    Core.shortcut_registry.add_shortcut(
        key_1=dpg.mvKey_Alt,
        key_2=dpg.mvKey_P,
        callback=test_shortcut
    )

    # At the end: assemble the registry
    Core.shortcut_registry.assemble_registry()