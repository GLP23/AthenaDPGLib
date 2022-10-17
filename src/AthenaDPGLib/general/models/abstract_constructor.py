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
    def _stage0_pre():
        """
        Stage 0 of the application constructor.
        This usually is the first stage to be called and generally prepares the environment for the application
        """

    @staticmethod
    @abstractmethod
    def _stage1_data():
        """
        Stage 1 of the application constructor.
        This usually creates data which has to be generated or called from a file
        """

    @staticmethod
    @abstractmethod
    def _stage2_functionality():
        """
        Stage 2 of the application constructor.
        This usually creates the models that interact with the data
        """

    @staticmethod
    @abstractmethod
    def _stage3_ui():
        """
        Stage 3 of the application constructor.
        This usually creates the UI models
        """

    @staticmethod
    @abstractmethod
    def _stage4_other():
        """
        Stage 4 of the application constructor.
        This doesn't have a defined stage subject,
            but is meant for other systems that have to be called upon after the ui has been defined, but before the ui
            will block the main thread
        """

    @staticmethod
    @abstractmethod
    def _stage5_blocking():
        """
        Stage 5 of the application constructor.
        This usually contains the main thread's blocking call of the ui
        """

    @staticmethod
    @abstractmethod
    def _stage6_shutdown():
        """
        Stage 6 of the application constructor.
        This usually contains the shutdown process of the application
        """
    @classmethod
    def construct(cls):
        """
        Method that controls the flow of construction of the application
        """
        if cls._constructed:
            raise PermissionError("Cannot construct an application multiple times")

        # set the attr to true,
        #   Can't construct an application twice
        cls._constructed = True

        # Startup all the static methods
        #   Sequence matters!
        cls._stage0_pre()
        cls._stage1_data()
        cls._stage2_functionality()
        cls._stage3_ui()
        cls._stage4_other()
        cls._stage5_blocking()
        cls._stage6_shutdown()
