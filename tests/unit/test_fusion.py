import numpy as np
import pytest

from ozon_dim.fusion import fuse_point_clouds


def test_fusion_applies_each_sensor_transform_before_concatenating() -> None:
    first = np.array([[0.0, 0.0, 0.0]], dtype=np.float64)
    second = np.array([[0.0, 0.0, 0.0]], dtype=np.float64)
    identity = np.eye(4, dtype=np.float64)
    translated = np.eye(4, dtype=np.float64)
    translated[0, 3] = 100.0

    fused = fuse_point_clouds([first, second], [identity, translated])

    np.testing.assert_array_equal(fused, np.array([[0.0, 0.0, 0.0], [100.0, 0.0, 0.0]]))


def test_fusion_rejects_a_mismatched_number_of_transforms() -> None:
    with pytest.raises(ValueError, match="same length"):
        fuse_point_clouds([np.empty((0, 3), dtype=np.float64)], [])
