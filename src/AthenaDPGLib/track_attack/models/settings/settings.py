# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
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
            filepath=filepath,
            # **json_kwargs
            indent=2
        )

    def register_hook(self, callback, setting:SettingsEnum):
        self._hooks[setting].append(callback)

    def get_hooks(self,setting:SettingsEnum) -> list[Callable]:
        return self._hooks[setting]

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties with their hooks -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def viewport_show_title(self):
        return self._values.viewport_show_title
    @viewport_show_title.setter
    @apply_settings_hooks_after_property_setter
    def viewport_show_title(self, value):
        self._values.viewport_show_title = value

    @property
    def viewport_width(self):
        return self._values.viewport_width
    @viewport_width.setter
    @apply_settings_hooks_after_property_setter
    def viewport_width(self, value):
        self._values.viewport_width = value

    @property
    def viewport_height(self):
        return self._values.viewport_height
    @viewport_height.setter
    @apply_settings_hooks_after_property_setter
    def viewport_height(self, value):
        self._values.viewport_height = value

    @property
    def viewport_x(self):
        return self._values.viewport_x
    @viewport_x.setter
    @apply_settings_hooks_after_property_setter
    def viewport_x(self, value):
        self._values.viewport_x = value

    @property
    def viewport_y(self):
        return self._values.viewport_y
    @viewport_y.setter
    @apply_settings_hooks_after_property_setter
    def viewport_y(self, value):
        self._values.viewport_y = value

    @property
    def viewport_vsync(self):
        return self._values.viewport_vsync
    @viewport_vsync.setter
    @apply_settings_hooks_after_property_setter
    def viewport_vsync(self, value):
        self._values.viewport_vsync = value

    @property
    def viewport_fullscreen(self):
        return self._values.viewport_fullscreen
    @viewport_fullscreen.setter
    @apply_settings_hooks_after_property_setter
    def viewport_fullscreen(self, value):
        self._values.viewport_fullscreen = value

    @property
    def debug_show(self):
        return self._values.debug_show
    @debug_show.setter
    @apply_settings_hooks_after_property_setter
    def debug_show(self, value):
        self._values.debug_show = value

    @property
    def metrics_show(self):
        return self._values.metrics_show
    @metrics_show.setter
    @apply_settings_hooks_after_property_setter
    def metrics_show(self, value):
        self._values.metrics_show = value

