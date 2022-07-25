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
@dataclass()
class FilePaths:
    icon:str=NOTHING

    @classmethod
    def from_file(cls, filepath:str):
        with open(filepath, "r") as file:
            kwargs_paths = json.load(file)
        return cls(**kwargs_paths)