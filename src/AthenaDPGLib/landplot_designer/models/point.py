# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, InitVar, field
import numpy as np
from numpy.typing import ArrayLike

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(init=False, slots=True)
class Point:
    _pos:ArrayLike

    def __init__(self, x:float, y:float):
        self._pos = np.array([x,y])

    @property
    def x(self):
        return self._pos[0]
    @property
    def y(self):
        return self._pos[1]

    def __hash__(self):
        return hash((self._pos[0], self._pos[1]))

    def __iter__(self):
        return iter(self._pos)