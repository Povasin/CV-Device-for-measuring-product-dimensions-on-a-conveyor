"""Small, deterministic offline measurement pipeline."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ozon_dim.geometry.bounding_box import approximate_oriented_bounding_box
from ozon_dim.measurement.validation import dimensions_within_operating_range
from ozon_dim.preprocessing.foreground import points_above_conveyor


class InsufficientObjectPointsError(ValueError):
    """Raised when no measurable three-dimensional object remains after filtering."""


@dataclass(frozen=True, slots=True)
class MeasurementResult:
    """Dimensions estimated from one already calibrated point cloud."""

    dimensions_mm: npt.NDArray[np.float64]
    point_count: int
    algorithm: str
    within_operating_range: bool


def measure_product(
    points_mm: npt.NDArray[np.float64], min_height_mm: float = 2.0
) -> MeasurementResult:
    """Remove conveyor points and calculate the baseline oriented bounding box.

    The returned algorithm is an approximation, not a verified globally exact MVBB.
    """
    object_points = points_above_conveyor(points_mm, min_height_mm=min_height_mm)
    if len(object_points) < 4:
        raise InsufficientObjectPointsError("at least four object points are required after filtering")
    box = approximate_oriented_bounding_box(object_points)
    return MeasurementResult(
        dimensions_mm=box.extents,
        point_count=len(object_points),
        algorithm=box.algorithm,
        within_operating_range=dimensions_within_operating_range(box.extents),
    )
