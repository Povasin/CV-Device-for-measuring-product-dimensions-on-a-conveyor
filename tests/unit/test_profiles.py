from __future__ import annotations

import numpy as np
import pytest

from ozon_dim.acquisition.profiles import LaserProfile, ProfileBundle


def test_laser_profile_preserves_validity_and_traceability() -> None:
    profile = LaserProfile(
        sensor_id="top",
        profile_index=42,
        captured_at_ns=1_700_000_000,
        encoder_count=1200,
        points_sensor_mm=np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]),
        valid_mask=np.array([True, False]),
        intensity=np.array([80.0, 0.0]),
        calibration_id="cal-2026-09-09",
    )

    np.testing.assert_array_equal(profile.valid_points_sensor_mm, [[1.0, 2.0, 3.0]])
    with pytest.raises(ValueError):
        profile.points_sensor_mm[0, 0] = 0.0


@pytest.mark.parametrize("sensor_id", ["", None])
def test_laser_profile_rejects_an_invalid_sensor_identifier(sensor_id: str | None) -> None:
    with pytest.raises(ValueError, match="sensor_id"):
        LaserProfile(
            sensor_id=sensor_id,  # type: ignore[arg-type]
            profile_index=0,
            captured_at_ns=1,
            encoder_count=0,
            points_sensor_mm=np.array([[1.0, 2.0, 3.0]]),
            valid_mask=np.array([True]),
            intensity=None,
            calibration_id="cal-1",
        )


@pytest.mark.parametrize(
    ("points", "valid_mask"),
    [
        (np.array([[1.0, 2.0, float("nan")]]), np.array([True])),
        (np.array([[1.0, 2.0, 3.0]]), np.array([True, False])),
    ],
)
def test_laser_profile_rejects_non_finite_points_and_mismatched_masks(
    points: np.ndarray, valid_mask: np.ndarray
) -> None:
    with pytest.raises(ValueError):
        LaserProfile(
            sensor_id="top",
            profile_index=0,
            captured_at_ns=1,
            encoder_count=0,
            points_sensor_mm=points,
            valid_mask=valid_mask,
            intensity=None,
            calibration_id="cal-1",
        )


def test_profile_bundle_records_missing_expected_sensor_for_later_rejection() -> None:
    profile = LaserProfile(
        sensor_id="top",
        profile_index=0,
        captured_at_ns=1,
        encoder_count=0,
        points_sensor_mm=np.array([[1.0, 2.0, 3.0]]),
        valid_mask=np.array([True]),
        intensity=None,
        calibration_id="cal-1",
    )

    bundle = ProfileBundle(
        event_id="event-1",
        required_sensor_ids=frozenset({"top", "left", "right"}),
        profiles=(profile,),
        missing_profile_count=0,
    )

    assert (
        bundle.capture_evidence.rejection_reason
        == "missing required sensor observations: left, right"
    )
