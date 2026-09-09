"""Evidence and object-cloud contracts used before geometry is measured."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


def _sensor_ids(sensor_ids: frozenset[str], field_name: str) -> frozenset[str]:
    values = frozenset(sensor_ids)
    if any(not isinstance(sensor_id, str) or not sensor_id.strip() for sensor_id in values):
        raise ValueError(f"{field_name} must contain only non-empty strings")
    return values


@dataclass(frozen=True, slots=True)
class CaptureEvidence:
    """Quality signals that prevent a partial object cloud from being measured."""

    required_sensor_ids: frozenset[str]
    observed_sensor_ids: frozenset[str]
    missing_profile_count: int
    touches_roi_boundary: bool
    component_count: int

    def __post_init__(self) -> None:
        required = _sensor_ids(self.required_sensor_ids, "required_sensor_ids")
        observed = _sensor_ids(self.observed_sensor_ids, "observed_sensor_ids")
        if not required:
            raise ValueError("required_sensor_ids must not be empty")
        if self.missing_profile_count < 0:
            raise ValueError("missing_profile_count must be non-negative")
        if self.component_count < 0:
            raise ValueError("component_count must be non-negative")
        object.__setattr__(self, "required_sensor_ids", required)
        object.__setattr__(self, "observed_sensor_ids", observed)

    @classmethod
    def complete(cls, sensor_ids: set[str]) -> CaptureEvidence:
        """Create evidence for a contiguous one-object capture from all sensors."""
        identifiers = frozenset(sensor_ids)
        return cls(identifiers, identifiers, 0, False, 1)

    @property
    def rejection_reason(self) -> str | None:
        """Return the first deterministic reason the capture cannot be measured."""
        missing = sorted(self.required_sensor_ids - self.observed_sensor_ids)
        if missing:
            return f"missing required sensor observations: {', '.join(missing)}"
        unexpected = sorted(self.observed_sensor_ids - self.required_sensor_ids)
        if unexpected:
            return f"unexpected sensor observations: {', '.join(unexpected)}"
        if self.missing_profile_count:
            return f"missing profile count: {self.missing_profile_count}"
        if self.touches_roi_boundary:
            return "object touches the measurement ROI boundary"
        if self.component_count != 1:
            return f"expected one object component, found {self.component_count}"
        return None


@dataclass(frozen=True, slots=True)
class ObjectObservation:
    """A calibrated, segmented product cloud and its completeness evidence.

    ``points_mm`` contains foreground points chosen by upstream background modelling;
    it may include object points at Z=0 and must not be filtered again by a fixed
    height threshold.
    """

    event_id: str
    points_mm: npt.NDArray[np.float64]
    evidence: CaptureEvidence

    def __post_init__(self) -> None:
        if not isinstance(self.event_id, str) or not self.event_id.strip():
            raise ValueError("event_id must be a non-empty string")
        points = np.asarray(self.points_mm, dtype=np.float64)
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("points_mm must have shape (N, 3)")
        if not np.all(np.isfinite(points)):
            raise ValueError("points_mm must contain only finite values")
        points = np.array(points, copy=True)
        points.setflags(write=False)
        object.__setattr__(self, "points_mm", points)
