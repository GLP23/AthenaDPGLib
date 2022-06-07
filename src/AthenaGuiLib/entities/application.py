# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, field

# Custom Library
from AthenaGuiLib.models import (AppInfo, AppSettings)
import AthenaGuiLib.res.strings as strings

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class Application:
    """
    Class to house all logic and data behind an application

    Order of calls:
        .viewport_define()

        .launch()

    """
    # Keyword arguments on init
    info: AppInfo = field(default_factory=AppInfo.factory)  # All info data is frozen across the instance of an application
    settings: AppSettings = field(default_factory=AppSettings.factory) # All settings can be changed while the application is running

    # class attributes not to be setup on init
    restart:bool = field(init=False, default=False)

    # ------------------------------------------------------------------------------------------------------------------
    # - Propeties -
    # ------------------------------------------------------------------------------------------------------------------
