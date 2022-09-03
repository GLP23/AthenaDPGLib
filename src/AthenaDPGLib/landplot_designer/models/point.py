# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass, InitVar, field
import numpy as np
from numpy.typing import ArrayLike
from typing import Iterator

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(init=False, slots=True)
class Point:
    _pos:ArrayLike

    def __init__(self, x:float=0., y:float=0.):
        self._pos = np.array([x,y])

    @classmethod
    def from_array(cls,array:ArrayLike) -> Point:
        obj = cls()
        obj._pos = array
        return obj

    @property
    def x(self) -> float:
        return self._pos[0]
    @property
    def y(self) -> float:
        return self._pos[1]

    @property
    def pos(self) -> ArrayLike:
        return self._pos

    def __hash__(self) -> int:
        return hash((self._pos[0], self._pos[1]))

    def __iter__(self)-> Iterator:
        return iter(self._pos)