from __future__ import annotations

import numpy as np
import pytest

from ozon_dim.acquisition.profiles import LaserProfile
from ozon_dim.acquisition.registration import register_profile_points


def test_registration_compensates_conveyor_motion_from_encoder_counts() -> None:
    profile = LaserProfile(
        sensor_id="top",
        profile_index=1,
        captured_at_ns=10,
        encoder_count=110,
        points_sensor_mm=np.array([[1.0, 2.0, 3.0], [9.0, 9.0, 9.0]]),
        valid_mask=np.array([True, False]),
        intensity=None,
        calibration_id="cal-1",
    )

    registered = register_profile_points(
        profile,
        np.eye(4),
        reference_encoder_count=100,
        mm_per_encoder_count=0.05,
    )

    np.testing.assert_allclose(registered, [[0.5, 2.0, 3.0]])


def test_registration_rejects_an_invalid_encoder_scale() -> None:
    profile = LaserProfile(
        sensor_id="top",
        profile_index=1,
        captured_at_ns=10,
        encoder_count=110,
        points_sensor_mm=np.array([[1.0, 2.0, 3.0]]),
        valid_mask=np.array([True]),
        intensity=None,
        calibration_id="cal-1",
    )

    with pytest.raises(ValueError, match="positive"):
        register_profile_points(profile, np.eye(4), 100, mm_per_encoder_count=0.0)
