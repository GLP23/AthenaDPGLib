# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaDPGLib.track_attack.models.core import Core

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
AS_HOOK = "_as_hook"

class HasSettingsHooks:
    """
    Class which is inherited by other class that need to have proper Setting hook interactions
    """
    def __new__(cls, *args, **kwargs):
        # create the object
        obj = super(HasSettingsHooks, cls).__new__(cls)
        # init the object
        # noinspection PyArgumentList
        obj.__init__(*args, **kwargs)

        for name in obj.__dir__():
            # need to check if the name of the attribute actually exists,
            # some attributes are populated later on
            if not hasattr(obj, name) or not hasattr((method := getattr(obj,name)), AS_HOOK):
                continue

            # register the method of the instanced object
            #   If you don't do this, the "self" arg won't ever be populated
            Core.settings.register_hook(callback=method, setting=getattr(method,AS_HOOK))

        return obj

