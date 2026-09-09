"""Encoder-based registration of sequential line profiles to a product frame."""

from __future__ import annotations

from collections.abc import Mapping
from numbers import Integral

import numpy as np
import numpy.typing as npt

from ozon_dim.acquisition.profiles import LaserProfile, ProfileBundle
from ozon_dim.geometry.transforms import transform_points
from ozon_dim.measurement.observation import CaptureEvidence, ObjectObservation
from ozon_dim.preprocessing.segmentation import (
    InsufficientObjectComponentError,
    MultipleObjectComponentsError,
    select_single_object_points,
)


def register_profile_points(
    profile: LaserProfile,
    sensor_to_conveyor: npt.NDArray[np.float64],
    reference_encoder_count: int,
    mm_per_encoder_count: float,
) -> npt.NDArray[np.float64]:
    """Register valid profile points to a stationary reference position.

    The conveyor coordinate system is X along belt motion, Y across the belt and Z
    upward from the belt. A positive encoder change means the belt advanced in +X,
    therefore the same physical product is shifted back by that distance.
    """
    scale = float(mm_per_encoder_count)
    if not np.isfinite(scale) or scale <= 0.0:
        raise ValueError("mm_per_encoder_count must be finite and positive")
    if isinstance(reference_encoder_count, bool) or not isinstance(
        reference_encoder_count, Integral
    ):
        raise TypeError("reference_encoder_count must be an integer")

    points = transform_points(profile.valid_points_sensor_mm, sensor_to_conveyor)
    displacement_mm = (profile.encoder_count - reference_encoder_count) * scale
    registered = np.array(points, copy=True)
    registered[:, 0] -= displacement_mm
    return registered


def _registered_bundle_points(
    bundle: ProfileBundle,
    sensor_to_conveyor: Mapping[str, npt.NDArray[np.float64]],
    reference_encoder_count: int,
    mm_per_encoder_count: float,
) -> npt.NDArray[np.float64]:
    registered_profiles: list[npt.NDArray[np.float64]] = []
    for profile in bundle.profiles:
        try:
            transform = sensor_to_conveyor[profile.sensor_id]
        except KeyError as error:
            raise ValueError(f"missing transform for sensor_id {profile.sensor_id!r}") from error
        registered_profiles.append(
            register_profile_points(
                profile, transform, reference_encoder_count, mm_per_encoder_count
            )
        )
    if not registered_profiles:
        return np.empty((0, 3), dtype=np.float64)
    return np.vstack(registered_profiles)


def _evidence_with_component_count(
    evidence: CaptureEvidence, component_count: int
) -> CaptureEvidence:
    return CaptureEvidence(
        required_sensor_ids=evidence.required_sensor_ids,
        observed_sensor_ids=evidence.observed_sensor_ids,
        missing_profile_count=evidence.missing_profile_count,
        touches_roi_boundary=evidence.touches_roi_boundary,
        component_count=component_count,
    )


def assemble_object_observation(
    bundle: ProfileBundle,
    sensor_to_conveyor: Mapping[str, npt.NDArray[np.float64]],
    reference_encoder_count: int,
    mm_per_encoder_count: float,
    max_neighbor_distance_mm: float,
    min_component_points: int,
) -> ObjectObservation:
    """Register a triggered profile bundle and produce one quality-gated object cloud.

    The function does not estimate inter-sensor calibration. It consumes the versioned
    rigid transforms supplied by the calibration process, applies encoder motion
    compensation, then rejects multi-product or unsupported foreground before OBB.
    """
    points = _registered_bundle_points(
        bundle, sensor_to_conveyor, reference_encoder_count, mm_per_encoder_count
    )
    evidence = bundle.capture_evidence
    if evidence.rejection_reason is not None:
        return ObjectObservation(bundle.event_id, points, evidence)
    try:
        selected_points = select_single_object_points(
            points, max_neighbor_distance_mm, min_component_points
        )
    except InsufficientObjectComponentError:
        return ObjectObservation(
            bundle.event_id, points, _evidence_with_component_count(evidence, component_count=0)
        )
    except MultipleObjectComponentsError:
        return ObjectObservation(
            bundle.event_id, points, _evidence_with_component_count(evidence, component_count=2)
        )
    return ObjectObservation(
        bundle.event_id,
        selected_points,
        _evidence_with_component_count(evidence, component_count=1),
    )
