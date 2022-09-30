# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import functools

# Custom Library

# Custom Packages
from AthenaDPGLib.track_attack.models.settings.values import SettingsEnum

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def register_settings_hook(setting: SettingsEnum):
    """
    Decorator for a class function that marks the function as a "to hook function"
    The class in question must inherit from the "HasSettingsHooks" class for it to take effect.
    """
    def decorator(fnc):
        # assign an attribute to the function,
        #   so the class "HasSettingsHooks" can find it
        fnc._as_hook = setting
        return fnc
    return decorator

def apply_settings_hooks_after_property_setter(fnc):
    """
    Decorator that automatically executes the hooks tied to a setting.
    The decorator is meant to decorator a setter of a property function in the Core.Settings class to work correctly
    """
    # the enum only has to be gathered once,
    #   don't get this every single time the setter is run.
    #   Will cause an attribute error if the setting hasn't been defined as an enum yet
    settings_enum = getattr(SettingsEnum, fnc.__name__)

    @functools.wraps(fnc)
    def wrapper(*args, **kwargs):
        # the properties aren't static- or class methods,
        #   so we always know the first arg is the "self"
        self, *_ = args
        result = fnc(*args, **kwargs) # first run the setter, as the hooks depend on the new value

        # executes the various hooks
        for hook in self.get_hooks(setting=settings_enum):
            hook()

        # even though a setter property doesn't return anything,
        #   keep convention and return result
        return result
    return wrapper