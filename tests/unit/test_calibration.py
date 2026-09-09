import numpy as np
import pytest

from ozon_dim.calibration import Calibration


def test_calibration_accepts_a_rigid_homogeneous_transform() -> None:
    transform = np.eye(4, dtype=np.float64)

    calibration = Calibration("cal-2026-01", transform)

    assert calibration.calibration_id == "cal-2026-01"
    np.testing.assert_array_equal(calibration.transform, transform)


def test_calibration_rejects_non_rigid_rotation() -> None:
    transform = np.eye(4, dtype=np.float64)
    transform[0, 0] = 2.0

    with pytest.raises(ValueError, match="orthonormal"):
        Calibration("cal-1", transform)


def test_calibration_rejects_a_non_finite_translation() -> None:
    transform = np.eye(4, dtype=np.float64)
    transform[0, 3] = np.nan

    with pytest.raises(ValueError, match="finite"):
        Calibration("cal-1", transform)


def test_calibration_keeps_an_immutable_copy_of_the_validated_transform() -> None:
    transform = np.eye(4, dtype=np.float64)
    calibration = Calibration("cal-1", transform)
    transform[0, 0] = 2.0

    np.testing.assert_array_equal(calibration.transform, np.eye(4, dtype=np.float64))
    with pytest.raises(ValueError):
        calibration.transform[0, 0] = 2.0
