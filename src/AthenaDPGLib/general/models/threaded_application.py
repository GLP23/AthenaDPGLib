# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Callable
import asyncio

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

    def run_in_thread(self, fnc, /, *args, **kwargs):
        return asyncio.run(self._ran_in_thread((fnc, args, kwargs)))

    async def _ran_in_thread(self, callback_setup:tuple[Callable, tuple, dict]):
        fnc, args, kwargs = callback_setup
        result = await asyncio.wrap_future(self._executor.submit(fnc, *args, **kwargs))
        return result

