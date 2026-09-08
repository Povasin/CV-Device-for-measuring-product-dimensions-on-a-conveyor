import numpy as np
import pytest

from ozon_dim.preprocessing.foreground import points_above_conveyor


def test_points_above_conveyor_keeps_only_object_points() -> None:
    points = np.array(
        [[0.0, 0.0, -1.0], [1.0, 1.0, 0.0], [2.0, 2.0, 2.1]], dtype=np.float64
    )

    actual = points_above_conveyor(points, conveyor_z_mm=0.0, min_height_mm=2.0)

    np.testing.assert_array_equal(actual, np.array([[2.0, 2.0, 2.1]], dtype=np.float64))


def test_points_above_conveyor_rejects_negative_height_threshold() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        points_above_conveyor(np.empty((0, 3), dtype=np.float64), min_height_mm=-0.1)
