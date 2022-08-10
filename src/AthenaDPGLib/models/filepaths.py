# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from dataclasses import dataclass
import json

# Custom Library
from AthenaLib.data.text import NOTHING

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True)
class FilePaths:
    icon:str=NOTHING

    @classmethod
    def from_json(cls, filepath:str):
        if not filepath.endswith(".json"):
            raise ValueError

        with open(filepath, "r") as file:
            kwargs_paths = json.load(file)
        return cls(**kwargs_paths)