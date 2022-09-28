# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaDPGLib.general.models.threaded_application import ThreadedExecutor

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
_threaded_executor: ThreadedExecutor | None = None

def get_threaded_executor()-> ThreadedExecutor:
    """
    A simple managed getter for the ThreadedExecutor object
    In one python instance, only one ThreadedExecutor is allowed to exist
    """

    global _threaded_executor

    if _threaded_executor is None:
        _threaded_executor = ThreadedExecutor()

    return _threaded_executor

