# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomDPGItem(ABC):
    @abstractmethod
    def dpg_constructor(self):
        """Main function which needs to be called to construct the dpg item"""

    # ------------------------------------------------------------------------------------------------------------------
    # - Context manager so the class can be used in a same manner as DPG functions -
    # ------------------------------------------------------------------------------------------------------------------
    def __enter__(self):
        self.dpg_constructor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass