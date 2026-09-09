import numpy as np
import pytest

from ozon_dim.pipeline import InsufficientObjectPointsError, measure_product


def test_pipeline_reports_insufficient_object_points_after_background_removal() -> None:
    points = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 0.0]], dtype=np.float64)

    with pytest.raises(InsufficientObjectPointsError, match="at least four"):
        measure_product(points)


def test_pipeline_reports_coplanar_object_points_without_leaking_a_qhull_error() -> None:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [20.0, 0.0, 0.0],
            [0.0, 20.0, 0.0],
            [20.0, 20.0, 0.0],
            [0.0, 0.0, 50.0],
            [20.0, 0.0, 50.0],
            [0.0, 20.0, 50.0],
            [20.0, 20.0, 50.0],
        ],
        dtype=np.float64,
    )

    with pytest.raises(InsufficientObjectPointsError, match="span three dimensions"):
        measure_product(points)
