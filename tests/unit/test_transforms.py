from __future__ import annotations

import numpy as np
import pytest

from ozon_dim.geometry.transforms import transform_points


def test_transform_points_returns_identity_transform_unchanged() -> None:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [10.0, -5.0, 2.5],
        ],
        dtype=np.float64,
    )

    result = transform_points(points, np.eye(4, dtype=np.float64))

    np.testing.assert_allclose(result, points)
    assert result.dtype == np.float64


def test_transform_points_rejects_non_homogeneous_transform() -> None:
    points = np.array([[1.0, 2.0, 3.0]], dtype=np.float64)

    with pytest.raises(ValueError, match=r"transform must have shape \(4, 4\)"):
        transform_points(points, np.eye(3, dtype=np.float64))


def test_transform_points_rejects_points_without_three_coordinates() -> None:
    invalid_points = np.array([[1.0, 2.0]], dtype=np.float64)

    with pytest.raises(ValueError, match=r"points must have shape \(N, 3\)"):
        transform_points(invalid_points, np.eye(4, dtype=np.float64))
