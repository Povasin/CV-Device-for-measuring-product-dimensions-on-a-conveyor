from pathlib import Path

import numpy as np
import pytest

from ozon_dim.acquisition.replay import load_laser_profile, load_point_cloud


def test_load_point_cloud_reads_float64_points_from_npz(tmp_path: Path) -> None:
    source = tmp_path / "frame.npz"
    np.savez(source, points_mm=np.array([[1, 2, 3]], dtype=np.float32))

    points = load_point_cloud(source)

    assert points.dtype == np.float64
    np.testing.assert_array_equal(points, np.array([[1.0, 2.0, 3.0]]))


def test_load_point_cloud_rejects_missing_points_key(tmp_path: Path) -> None:
    source = tmp_path / "invalid.npz"
    np.savez(source, depth=np.array([1]))

    with pytest.raises(ValueError, match="points_mm"):
        load_point_cloud(source)


def test_load_laser_profile_uses_the_same_contract_as_a_live_adapter(tmp_path: Path) -> None:
    source = tmp_path / "profile.npz"
    np.savez(
        source,
        sensor_id=np.array("top"),
        profile_index=np.array(3),
        captured_at_ns=np.array(99),
        encoder_count=np.array(1234),
        points_sensor_mm=np.array([[1.0, 2.0, 3.0]]),
        valid_mask=np.array([True]),
        intensity=np.array([87.0]),
        calibration_id=np.array("cal-1"),
    )

    profile = load_laser_profile(source)

    assert profile.sensor_id == "top"
    assert profile.profile_index == 3
    assert profile.encoder_count == 1234
    np.testing.assert_array_equal(profile.valid_points_sensor_mm, [[1.0, 2.0, 3.0]])
