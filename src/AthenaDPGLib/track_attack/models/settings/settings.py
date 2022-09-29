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
from AthenaLib.general.functions.decorators import empty_decorator

# Custom Packages
from AthenaDPGLib.track_attack.models.settings.values import SettingValues, SettingEnum

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Settings:
    # None Init
    _values: SettingValues = field(init=False, default_factory=SettingValues)
    _hooks:dict[SettingEnum:list[Callable]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        for setting_enum in SettingEnum:
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

        self._values = SettingValues(**load_jsonfile(filepath=filepath))

    def dump_to_file(self, filepath:PATHLIKE):
        """
        Method that dumps the self._values to the given settings file.
        Has the option to dump out to another filepath than the stored self._json_file
        """
        dump_dataclass_to_jsonfile(
            obj=self._values,
            filepath=filepath
        )

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties with their hooks -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def show_viewport_title(self):
        return self._values.show_viewport_title
    @show_viewport_title.setter
    def show_viewport_title(self, value):
        self._values.show_viewport_title = value
        print(self._hooks)
        # todo how in the hell do I do this automatically?
        for hook in self._hooks[SettingEnum.show_viewport_title]:
            hook()

    def assign_as_hook(self, hook_to_attr:SettingEnum):
        # uses the "empty_decorator" from AthenaLib
        #   This is just a decorator that functions as normal
        #   Doesn't do anything special
        def decorator(fnc):
            self._hooks[hook_to_attr].append(fnc)

            @functools.wraps(fnc)
            def wrapper(*args, **kwargs):
                return fnc(*args, **kwargs)

            return wrapper
        return decorator


