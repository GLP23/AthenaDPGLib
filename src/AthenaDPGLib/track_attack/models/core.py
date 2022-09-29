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
from AthenaDPGLib.track_attack.models.settings.settings import Settings

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Core(GlobalCore):
    # data components
    settings:ClassVar[Settings] = Settings() # because decorators depend on it
    texture_registry:CV_UNDEFINED
    shortcut_registry:CV_UNDEFINED

    # functionality components
    threaded_executor:ClassVar[ThreadedExecutor] = ThreadedExecutor() # because decorators depend on it
    data_tracker:CV_UNDEFINED

    # ui components
    ui_track_attack: CV_UNDEFINED
    ui_viewport:CV_UNDEFINED
