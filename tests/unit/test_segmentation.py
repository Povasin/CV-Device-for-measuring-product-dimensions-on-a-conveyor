from __future__ import annotations

import numpy as np
import pytest

from ozon_dim.preprocessing.segmentation import (
    MultipleObjectComponentsError,
    select_single_object_points,
)


def _cube_points(offset_x_mm: float = 0.0) -> np.ndarray:
    values = np.array([0.0, 10.0, 20.0])
    x, y, z = np.meshgrid(values + offset_x_mm, values, values, indexing="ij")
    return np.column_stack((x.ravel(), y.ravel(), z.ravel()))


def test_segmentation_removes_an_isolated_outlier_before_measuring() -> None:
    points = np.vstack((_cube_points(), np.array([[200.0, 200.0, 200.0]])))

    selected = select_single_object_points(
        points, max_neighbor_distance_mm=18.0, min_component_points=4
    )

    assert selected.shape == (27, 3)
    np.testing.assert_allclose(selected.max(axis=0), [20.0, 20.0, 20.0])


def test_segmentation_rejects_two_separate_products() -> None:
    points = np.vstack((_cube_points(), _cube_points(offset_x_mm=100.0)))

    with pytest.raises(MultipleObjectComponentsError, match="multiple object components"):
        select_single_object_points(points, max_neighbor_distance_mm=18.0, min_component_points=4)
