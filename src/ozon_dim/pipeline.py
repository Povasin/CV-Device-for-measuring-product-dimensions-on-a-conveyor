"""Small, deterministic offline measurement pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np
import numpy.typing as npt

from ozon_dim.geometry.bounding_box import approximate_oriented_bounding_box
from ozon_dim.measurement.observation import ObjectObservation
from ozon_dim.measurement.validation import dimensions_within_operating_range
from ozon_dim.preprocessing.foreground import points_above_conveyor


class InsufficientObjectPointsError(ValueError):
    """Raised when no measurable three-dimensional object remains after filtering."""


class MeasurementStatus(StrEnum):
    """Disposition of a measurement event before any WMS delivery attempt."""

    VALID = "valid"
    REJECTED = "rejected"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class MeasurementResult:
    """Dimensions or an explicit reason why an event cannot be measured."""

    dimensions_mm: npt.NDArray[np.float64] | None
    point_count: int
    algorithm: str | None
    within_operating_range: bool
    status: MeasurementStatus
    reason: str | None
    center_mm: npt.NDArray[np.float64] | None
    rotation: npt.NDArray[np.float64] | None


def _valid_result(points: npt.NDArray[np.float64]) -> MeasurementResult:
    box = approximate_oriented_bounding_box(points)
    return MeasurementResult(
        dimensions_mm=box.extents,
        point_count=len(points),
        algorithm=box.algorithm,
        within_operating_range=dimensions_within_operating_range(box.extents),
        status=MeasurementStatus.VALID,
        reason=None,
        center_mm=box.center,
        rotation=box.rotation,
    )


def _rejected_result(point_count: int, reason: str) -> MeasurementResult:
    return MeasurementResult(
        dimensions_mm=None,
        point_count=point_count,
        algorithm=None,
        within_operating_range=False,
        status=MeasurementStatus.REJECTED,
        reason=reason,
        center_mm=None,
        rotation=None,
    )


def measure_observation(observation: ObjectObservation) -> MeasurementResult:
    """Measure an already segmented cloud only when its capture evidence is complete."""
    if reason := observation.evidence.rejection_reason:
        return _rejected_result(len(observation.points_mm), reason)
    if len(observation.points_mm) < 4:
        return _rejected_result(
            len(observation.points_mm), "at least four object points are required"
        )
    try:
        return _valid_result(observation.points_mm)
    except ValueError as error:
        return _rejected_result(len(observation.points_mm), str(error))


def measure_product(
    points_mm: npt.NDArray[np.float64], min_height_mm: float = 2.0
) -> MeasurementResult:
    """Remove conveyor points and calculate the baseline oriented bounding box.

    The returned algorithm is an approximation, not a verified globally exact MVBB.
    """
    object_points = points_above_conveyor(points_mm, min_height_mm=min_height_mm)
    if len(object_points) < 4:
        raise InsufficientObjectPointsError(
            "at least four object points are required after filtering"
        )
    try:
        return _valid_result(object_points)
    except ValueError as error:
        raise InsufficientObjectPointsError(str(error)) from error
