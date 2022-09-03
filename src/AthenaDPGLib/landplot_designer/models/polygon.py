# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from numpy.typing import ArrayLike

# Custom Library
from AthenaLib.constants.types import COLOR
from AthenaColor.data.colors_html import DARKRED, ROYALBLUE

# Custom Packages
from AthenaDPGLib.landplot_designer.models.point import Point
from AthenaDPGLib.landplot_designer.functions.array_math import calculate_center, calculate_largest_radius

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Polygon:
    points:ArrayLike = field(default_factory=lambda:np.array([0.,0.]))
    origin:ArrayLike = field(default_factory=lambda:np.array([0.,0.]))

    color_fill:COLOR = field(default=ROYALBLUE)
    color_border:COLOR = field(default=ROYALBLUE)
    color_origin:COLOR = field(default=DARKRED)

    # - non init - (delayed as they are calculated on __post_init__)
    points_absolute:ArrayLike = field(init=False)
    largest_radius:float= field(init=False)

    def __post_init__(self):
        self.recalculate()

    # ------------------------------------------------------------------------------------------------------------------
    # - Class-methods that create new objects -
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def new_from_local(cls, origin:np.ndarray, points:np.ndarray,**kwargs) -> Polygon:
        """
        Use this if the origin is known and the points adjusted to the origin are known
        """
        return Polygon(
            origin=origin,
            points=points,
            **kwargs
        )

    @classmethod
    def new_from_absolute(cls, points:np.ndarray,**kwargs) -> Polygon:
        """
        Use this is you only know the absolute points of the polygon
        """
        if "origin" in kwargs:
            kwargs.pop("origin")

        poly = Polygon(
            points=points,
            **kwargs
        )
        poly.origin = calculate_center(poly.points)
        poly.points = poly.points - poly.origin
        poly.recalculate()
        return poly

    # ------------------------------------------------------------------------------------------------------------------
    # - Calculation of object variables -
    # ------------------------------------------------------------------------------------------------------------------
    def recalculate(self):
        """
        A collection of calculations to update the points around the origin
        """
        #Precalculated variable for the class
        # Done because the custom_series can now just reference the outcome instead of calculating it
        # Calculates the local points as absolute points,
        #     compared to the origin
        self.points_absolute = self.points + self.origin

        # Largest radius is needed for rendering distance checks
        self.largest_radius = calculate_largest_radius(self.origin, self.points_absolute)

    # ------------------------------------------------------------------------------------------------------------------
    # - Changes to the points array -
    # ------------------------------------------------------------------------------------------------------------------
    def add_local_point(self, pos:Point):
        self.points = np.append(self.points, [[pos.x, pos.y]], axis=0)
        self.recalculate()

    def add_absolute_point(self, pos:Point):
        pos_:np.ndarray = np.array([pos.x, pos.y])
        self.points = np.append(self.points, pos_-self.origin, axis=0)
        self.recalculate()

