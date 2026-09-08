import numpy as np

from ozon_dim.pipeline import measure_product


def test_pipeline_removes_conveyor_and_measures_a_rectangular_product() -> None:
    product = np.array(
        [
            [0.0, 0.0, 10.0], [200.0, 0.0, 10.0], [0.0, 100.0, 10.0], [200.0, 100.0, 10.0],
            [0.0, 0.0, 60.0], [200.0, 0.0, 60.0], [0.0, 100.0, 60.0], [200.0, 100.0, 60.0],
        ],
        dtype=np.float64,
    )
    conveyor = np.array([[0.0, 0.0, 0.0], [200.0, 100.0, 0.0]], dtype=np.float64)

    result = measure_product(np.vstack((product, conveyor)))

    assert result.point_count == 8
    assert result.algorithm == "open3d-face-aligned-approx"
    assert result.within_operating_range is True
    np.testing.assert_allclose(np.sort(result.dimensions_mm), [50.0, 100.0, 200.0])
