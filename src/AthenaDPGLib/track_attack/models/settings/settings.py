# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import functools
from dataclasses import dataclass, field
import pathlib
from typing import Callable

# Custom Library
from AthenaLib.constants.types import PATHLIKE
from AthenaLib.general.functions.json import load_jsonfile, dump_dataclass_to_jsonfile

# Custom Packages
from AthenaDPGLib.track_attack.models.settings.values import SettingsValues, SettingsEnum
from AthenaDPGLib.track_attack.functions.decorations import apply_settings_hooks_after_property_setter

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Settings:
    # None Init
    _values: SettingsValues = field(init=False, default_factory=SettingsValues)
    _hooks: dict[SettingsEnum:list[Callable]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        for setting_enum in SettingsEnum:
            # create empty record in the dictionary
            #   This is to prep the hook assembly
            self._hooks[setting_enum] = []

    # ------------------------------------------------------------------------------------------------------------------
    # - Functionality -
    # ------------------------------------------------------------------------------------------------------------------
    def load_from_file(self, filepath:PATHLIKE):
        # Load from file
        #   If the file doesn't exist, use some form of "default" settings
        if not pathlib.Path(filepath).exists():
            return # todo maybe this shouldn't be a silent error...

        self._values = SettingsValues(**load_jsonfile(filepath=filepath))

    def dump_to_file(self, filepath:PATHLIKE):
        """
        Method that dumps the self._values to the given settings file.
        Has the option to dump out to another filepath than the stored self._json_file
        """
        dump_dataclass_to_jsonfile(
            obj=self._values,
            filepath=filepath
        )

    def register_hook(self, callback, setting:SettingsEnum):
        self._hooks[setting].append(callback)

    def get_hooks(self,setting:SettingsEnum) -> list[Callable]:
        return self._hooks[setting]

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties with their hooks -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def show_viewport_title(self):
        return self._values.show_viewport_title

    @show_viewport_title.setter
    @apply_settings_hooks_after_property_setter
    def show_viewport_title(self, value):
        self._values.show_viewport_title = value
