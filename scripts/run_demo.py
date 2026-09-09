"""Run the deterministic offline demo from the repository root."""

import numpy as np

from ozon_dim.demo import synthetic_product_cloud
from ozon_dim.pipeline import measure_product

if __name__ == "__main__":
    result = measure_product(synthetic_product_cloud((200.0, 100.0, 50.0)))
    if result.dimensions_mm is None:
        raise RuntimeError(f"synthetic demo was rejected: {result.reason}")
    print(f"dimensions_mm={np.sort(result.dimensions_mm).tolist()}")
    print(f"point_count={result.point_count}")
    print(f"algorithm={result.algorithm}")
