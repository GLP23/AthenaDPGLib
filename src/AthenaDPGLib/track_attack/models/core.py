# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import ClassVar

# Custom Library
from AthenaLib.constants.types import CV_UNDEFINED

# Custom Packages
from AthenaDPGLib.general.models.global_core import GlobalCore
from AthenaDPGLib.general.models.threaded_application import ThreadedExecutor

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Core(GlobalCore):
    # data components

    # functionality components
    threaded_executor:ClassVar[ThreadedExecutor]
    data_tracker:CV_UNDEFINED

    # ui components
    ui_root: CV_UNDEFINED
