import numpy as np

from ozon_dim.demo import synthetic_product_cloud
from ozon_dim.pipeline import measure_product


def test_synthetic_demo_cloud_can_run_through_complete_pipeline() -> None:
    result = measure_product(synthetic_product_cloud((200.0, 100.0, 50.0)))

    np.testing.assert_allclose(np.sort(result.dimensions_mm), [50.0, 100.0, 200.0])
    assert result.point_count == 8
