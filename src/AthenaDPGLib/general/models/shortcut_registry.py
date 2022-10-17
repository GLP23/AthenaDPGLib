# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field, InitVar
import dearpygui.dearpygui as dpg
from typing import Callable

# Custom Library

# Custom Packages
from AthenaDPGLib.general.data.universal_tags import UniversalTags

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class ShortcutRegistry:
    # post init vars
    tag: InitVar[str | UniversalTags]

    # non init
    _registry: str | int = field(init=False)
    _key_combo_layout:dict[int:dict[int:Callable]] = field(init=False, default_factory=dict)

    def __post_init__(self, tag: str | UniversalTags):
        self._registry = dpg.add_handler_registry(tag=tag)

    def add_shortcut(self, key_1:int, key_2:int, callback:Callable):
        """
        Quick solution to add shortcut callbacks, which only take two keys to trigger
        """
        if key_1 not in self._key_combo_layout:
            self._key_combo_layout[key_1] = {}

        self._key_combo_layout[key_1][key_2] = callback

    def assemble_registry(self):
        """
        Has to be called at a certain point in the application construction for the item handlers to be applied.
        Make sure to run this function after all shortcuts have been added
        """
        # STUPID AND QUICK SOLUTION
        #   I don't care about this anymore, if you want shortcuts with more than two combinations:
        #       you can go figure it out yourself!
        def _options_callbacks(o: dict[int:Callable]):
            for key_2, callback in o.items():
                if dpg.is_key_pressed(key_2):
                    callback()
                    break

        for key_1, options in self._key_combo_layout.items():
            dpg.add_key_down_handler(
                key=key_1,
                callback=lambda: _options_callbacks(options),
                parent=self._registry
            )
