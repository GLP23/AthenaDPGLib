# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import overload


# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass()
class ThreadedExecutor:
    _executor:ThreadPoolExecutor = field(init=False, default_factory=ThreadPoolExecutor)

    def shutdown(self):
        self._executor.shutdown()

    def threaded_method(self, fnc):
        def decorator(*args, **kwargs):
            return self._executor.submit(fnc, *args, **kwargs)
        return decorator

