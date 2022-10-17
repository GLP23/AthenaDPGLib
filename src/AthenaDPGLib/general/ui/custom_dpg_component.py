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
class CustomDPGComponent(ABC):
    def add_dpg(self):
        """
        If the user doesn't need to extend the window's functionality, this method can be used to immediately run the
        dpg functions, without having to manually use a with statement
        """
        with self.dpg():
            pass

    @abstractmethod
    def dpg(self):
        """
        Context managed method, so that the user can extend the window's functionality with ease.
        """
        pass