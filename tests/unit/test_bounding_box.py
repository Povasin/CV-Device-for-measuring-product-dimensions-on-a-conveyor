from __future__ import annotations

import numpy as np
import pytest

from ozon_dim.geometry.bounding_box import approximate_oriented_bounding_box


def test_approximate_oriented_bounding_box_returns_extents_of_axis_aligned_box() -> None:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
            [0.0, 100.0, 0.0],
            [200.0, 100.0, 0.0],
            [0.0, 0.0, 50.0],
            [200.0, 0.0, 50.0],
            [0.0, 100.0, 50.0],
            [200.0, 100.0, 50.0],
        ],
        dtype=np.float64,
    )

    box = approximate_oriented_bounding_box(points)

    np.testing.assert_allclose(np.sort(box.extents), np.array([50.0, 100.0, 200.0]))
    np.testing.assert_allclose(box.center, np.array([100.0, 50.0, 25.0]))
    assert box.algorithm == "open3d-face-aligned-approx"


def test_approximate_oriented_bounding_box_rejects_less_than_four_points() -> None:
    points = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [2.0, 2.0, 2.0]], dtype=np.float64)

    with pytest.raises(ValueError, match="at least four points"):
        approximate_oriented_bounding_box(points)
