# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import ctypes
from dataclasses import dataclass, field
import json

# Custom Library
from AthenaLib.FileFolderManipulation import FileManipulation

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class AppVersion:
    Major: int|str
    Minor: int|str
    Patch: int|str

    @classmethod
    def generate_empty(cls) -> AppVersion:
        return cls(0,0,0)

    def __str__(self):
        return '.'.join(str(v) for v in self.__iter__())

    def __iter__(self):
        yield self.Major
        yield self.Minor
        yield self.Minor

    def to_dict(self) -> dict:
        return {
            "Major": self.Major,
            "Minor": self.Minor,
            "Patch": self.Patch
        }
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class AppInfo:
    path:str=None

    _empty:bool=field(default=False)
    _dictionary:dict = field(init=False)
    _version:AppVersion=field(init=False, default=None)

    def __post_init__(self):
        if not self._empty:
            # Make sure the file exists, else we raise an error
            FileManipulation(fatal=True).exists(self.path)

            # Read the file, if it exists and store dict
            with open(self.path, "r") as file:
                self._dictionary = json.load(file)
        else:
            with open("AthenaGuiLib/Applications/ApplicationInfo_Empty.json", "r") as file:
                self._dictionary = json.load(file)

    # ------------------------------------------------------------------------------------------------------------------
    # - Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def version(self):
        if self._version is None:
            version_dict:dict = self._dictionary["Version"]
            self._version = AppVersion(version_dict["Major"], version_dict["Minor"], version_dict["Patch"])
        return self._version

    @property
    def name(self):
        return self._dictionary["Name"]

    @property
    def icon(self):
        return self._dictionary["IconPath"]

    # ------------------------------------------------------------------------------------------------------------------
    # - Outputs -
    # ------------------------------------------------------------------------------------------------------------------
    def to_dict(self) -> dict:
        return self._dictionary

    def to_json_file(self, path=None, *, indent=4):
        if path is None:
            path = self.path
        with open(path, "w") as file:
            json.dump(
                self._dictionary,
                file,
                indent=indent
            )
