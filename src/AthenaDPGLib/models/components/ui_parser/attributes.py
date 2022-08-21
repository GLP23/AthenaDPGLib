# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import collections.abc
from typing import Any, Callable
from dataclasses import dataclass, InitVar, field

# Custom Library

# Custom Packages
from AthenaDPGLib.data.dpg_policies import DPG_TABLE_POLICIES
from AthenaDPGLib.data.text import POLICY, TABLE

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
FIX_DPG_KWARG_MAPPING: dict[str:dict[str:Callable]] = {}

def dpg_kwarg_fix(item:str, dpg_kwarg:str):
    def decorator(fnc):
        # always make sure we have a dictionary to place our key:Callable fix into it
        if item not in FIX_DPG_KWARG_MAPPING:
            FIX_DPG_KWARG_MAPPING[item] = {}

        if dpg_kwarg in FIX_DPG_KWARG_MAPPING[item]:
            raise ValueError(f"duplicate key : `{dpg_kwarg}` in FIX_ATTRIB_MAPPING[{item}]")

        # actually store the function
        FIX_DPG_KWARG_MAPPING[item][dpg_kwarg] = fnc
    return decorator

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class Attributes(collections.abc.Mapping):
    """
    Class which holds all the attributes of an item.
    Will fix any attributes that have to be mapped to another non-JSON-Storable data type
    """

    item:str # custom item name I've given to the dpg items to be used in json files
    attrib:InitVar[dict[str:Any]]

    # non init stuff
    _attrib:dict[str:Any] = field(init=False, default_factory=dict)

    def __post_init__(self, attrib: dict[str:Any]):
        for k, v in attrib.items():
            if k.startswith("_"):
                continue
            if self.item in FIX_DPG_KWARG_MAPPING and k in FIX_DPG_KWARG_MAPPING[self.item]:
                self._attrib[k] = FIX_DPG_KWARG_MAPPING[self.item][k](v)
            else:
                self._attrib[k] = v

    # ------------------------------------------------------------------------------------------------------------------
    # - Mapping abstract methods - (this way we can 'unpack' the Attributes Class)
    # ------------------------------------------------------------------------------------------------------------------
    def __iter__(self):
        return iter(self._attrib.keys()) # thanks for eivl in showing me collections.abc.Mapping

    def __getitem__(self, key):
        return self._attrib[key]

    def __len__(self):
        return len(self._attrib)

    # ------------------------------------------------------------------------------------------------------------------
    # - Kwarg fixes -
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    @dpg_kwarg_fix(item=TABLE, dpg_kwarg=POLICY)
    def fix_TablePolicy(value:str|int) -> int:
        if (value_ := value.lower() if isinstance(value, str) else value) in DPG_TABLE_POLICIES:
            return DPG_TABLE_POLICIES[value_]
        # Make sure the script actually raises an error, else it might cause unintended consequences
        #   NEVER error silently
        raise ValueError(f"value of `{value_}` could not be found in DPG_TABLE_POLICIES")

