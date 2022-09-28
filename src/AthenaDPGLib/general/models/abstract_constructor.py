# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar

# Custom Library

# Custom Packages


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class AbstractConstructor(ABC):
    _constructed:ClassVar[bool]=False

    @staticmethod
    @abstractmethod
    def _data():
        """
        Create data which have to be generated or called from a file before functionality and ui are created
        """

    @staticmethod
    @abstractmethod
    def _functionality():
        """
        Create the models that interact with the data
        """

    @staticmethod
    @abstractmethod
    def _ui():
        """
        Creates the UI models
        """

    @classmethod
    def construct(cls):
        if cls._constructed:
            raise PermissionError("Cannot construct an application multiple times")

        cls._data()
        cls._functionality()
        cls._ui()
