# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field, InitVar

# Custom Library

# Custom Packages
from AthenaDPGLib.landplot_designer.models.point import Point

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Polygon:
    points:np.ndarray = field(default_factory=lambda:np.ndarray([[0.,0.]]))
    origin:np.ndarray = field(default_factory=lambda:np.ndarray([0.,0.]))

    # - non init -
    points_absolute:np.ndarray = field(init=False)

    def __post_init__(self):
        self.calculate_points_as_absolute()

    def recalculate(self):
        self.calculate_origin()
        self.calculate_points_as_absolute()

    def calculate_origin(self):
        self.origin = np.array([
            self.points[:, 0].sum() / (length := len(self.points)),
            self.points[:, 1].sum() / length
        ])

    def calculate_points_as_local(self):
        self.points = self.points - self.origin

    def calculate_points_as_absolute(self):
        self.points_absolute = self.points + self.origin

    def add_local_point(self, pos:Point):
        self.points = np.append(self.points, [[pos.x, pos.y]], axis=0)

    def add_absolute_point(self, pos:Point):
        pos_:np.ndarray = np.array([pos.x, pos.y])
        self.points = np.append(self.points, pos_-self.origin, axis=0)

        self.recalculate()


    @classmethod
    def new_from_local(cls, origin:np.ndarray, points:np.ndarray) -> Polygon:
        """
        Use this if the origin is known and the points adjusted to the origin are known
        """
        return Polygon(
            origin=origin,
            points=points
        )

    @classmethod
    def new_from_absolute(cls, points:np.ndarray) -> Polygon:
        """
        Use this is you only know the absolute points of the polygon
        """
        poly = Polygon(
            points=points,
        )
        poly.recalculate()
        return poly

