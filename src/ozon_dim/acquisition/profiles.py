"""Contracts shared by a live line-profiler adapter and an offline replay adapter."""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Integral
from typing import Self

import numpy as np
import numpy.typing as npt

from ozon_dim.measurement.observation import CaptureEvidence


def _non_empty_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def _validated_sensor_ids(sensor_ids: frozenset[str]) -> frozenset[str]:
    values = frozenset(sensor_ids)
    if not values or any(
        not isinstance(sensor_id, str) or not sensor_id.strip() for sensor_id in values
    ):
        raise ValueError("sensor ids must be a non-empty set of non-empty strings")
    return values


@dataclass(frozen=True, slots=True)
class LaserProfile:
    """One line-profile acquisition with position and calibration traceability.

    Coordinates are in the sensor's calibrated local frame and millimetres. Invalid
    samples remain in the array only when their corresponding validity bit is false.
    """

    sensor_id: str
    profile_index: int
    captured_at_ns: int
    encoder_count: int
    points_sensor_mm: npt.NDArray[np.float64]
    valid_mask: npt.NDArray[np.bool_]
    intensity: npt.NDArray[np.float64] | None
    calibration_id: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "sensor_id", _non_empty_text(self.sensor_id, "sensor_id"))
        object.__setattr__(
            self, "calibration_id", _non_empty_text(self.calibration_id, "calibration_id")
        )
        for field_name, value in (
            ("profile_index", self.profile_index),
            ("captured_at_ns", self.captured_at_ns),
            ("encoder_count", self.encoder_count),
        ):
            if not isinstance(value, Integral) or isinstance(value, bool):
                raise TypeError(f"{field_name} must be an integer")
        if self.profile_index < 0 or self.captured_at_ns < 0:
            raise ValueError("profile_index and captured_at_ns must be non-negative")

        points = np.asarray(self.points_sensor_mm, dtype=np.float64)
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("points_sensor_mm must have shape (N, 3)")
        if not np.all(np.isfinite(points)):
            raise ValueError("points_sensor_mm must contain only finite values")
        mask = np.asarray(self.valid_mask, dtype=np.bool_)
        if mask.shape != (points.shape[0],):
            raise ValueError("valid_mask must have one value for every profile point")

        normalized_intensity: npt.NDArray[np.float64] | None = None
        if self.intensity is not None:
            normalized_intensity = np.asarray(self.intensity, dtype=np.float64)
            if normalized_intensity.shape != (points.shape[0],):
                raise ValueError("intensity must have one value for every profile point")
            if not np.all(np.isfinite(normalized_intensity)):
                raise ValueError("intensity must contain only finite values")

        points = np.array(points, copy=True)
        mask = np.array(mask, copy=True)
        points.setflags(write=False)
        mask.setflags(write=False)
        object.__setattr__(self, "points_sensor_mm", points)
        object.__setattr__(self, "valid_mask", mask)
        if normalized_intensity is not None:
            normalized_intensity = np.array(normalized_intensity, copy=True)
            normalized_intensity.setflags(write=False)
        object.__setattr__(self, "intensity", normalized_intensity)

    @property
    def valid_points_sensor_mm(self) -> npt.NDArray[np.float64]:
        """Return the finite coordinates selected by the sensor validity mask."""
        return self.points_sensor_mm[self.valid_mask]


@dataclass(frozen=True, slots=True)
class ProfileBundle:
    """All profiles retained for one triggered product event.

    Missing sensors or profile gaps are retained as evidence so the measurement
    stage can emit a recoverable rejection rather than silently treating a partial
    cloud as a complete product.
    """

    event_id: str
    required_sensor_ids: frozenset[str]
    profiles: tuple[LaserProfile, ...]
    missing_profile_count: int
    touches_roi_boundary: bool = False
    component_count: int = 1

    def __post_init__(self) -> None:
        object.__setattr__(self, "event_id", _non_empty_text(self.event_id, "event_id"))
        required = _validated_sensor_ids(self.required_sensor_ids)
        profiles = tuple(self.profiles)
        if not profiles:
            raise ValueError("profiles must not be empty")
        if self.missing_profile_count < 0:
            raise ValueError("missing_profile_count must be non-negative")
        if self.component_count < 0:
            raise ValueError("component_count must be non-negative")
        keys = {(profile.sensor_id, profile.profile_index) for profile in profiles}
        if len(keys) != len(profiles):
            raise ValueError("profiles must not repeat a sensor_id and profile_index pair")
        object.__setattr__(self, "required_sensor_ids", required)
        object.__setattr__(self, "profiles", profiles)

    @property
    def observed_sensor_ids(self) -> frozenset[str]:
        """Return sensor ids that supplied at least one retained profile."""
        return frozenset(profile.sensor_id for profile in self.profiles)

    @property
    def capture_evidence(self) -> CaptureEvidence:
        """Translate raw-capture completeness into the measurement quality contract."""
        return CaptureEvidence(
            required_sensor_ids=self.required_sensor_ids,
            observed_sensor_ids=self.observed_sensor_ids,
            missing_profile_count=self.missing_profile_count,
            touches_roi_boundary=self.touches_roi_boundary,
            component_count=self.component_count,
        )

    @classmethod
    def from_profiles(
        cls,
        event_id: str,
        required_sensor_ids: frozenset[str],
        profiles: tuple[LaserProfile, ...],
    ) -> Self:
        """Create a complete-capture candidate; drivers must report known gaps explicitly."""
        return cls(event_id, required_sensor_ids, profiles, missing_profile_count=0)
