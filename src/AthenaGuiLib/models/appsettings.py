# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(
    eq=False, # no need for equal check
    kw_only=True,
    slots=True
)
class AppSettings:
    """
    Application Settings class, houses all the changable information of an application
    Aka: fullscreen state, position, etc
    """
    fullscreen:bool = False
    width:int = 255
    height:int = 255
    x_pos:int = 0
    y_pos:int = 0

    def _export_to_dict_other(self) -> dict[str:Any]:
        """
        Method used to make sure other defined settings can be exported as well.
        This needs to be populated if there are other settings set
        :return:
        """
        pass

    def export_to_dict(self) -> dict[str:Any]:
        return {
            "fullscreen": self.fullscreen,
            **self._export_to_dict_other()
        }

    @classmethod
    def factory(cls) -> AppSettings:
        return AppSettings()
