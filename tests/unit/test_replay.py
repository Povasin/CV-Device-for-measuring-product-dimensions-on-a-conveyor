from pathlib import Path

import numpy as np
import pytest

from ozon_dim.acquisition.replay import load_point_cloud


def test_load_point_cloud_reads_float64_points_from_npz(tmp_path: Path) -> None:
    source = tmp_path / "frame.npz"
    np.savez(source, points_mm=np.array([[1, 2, 3]], dtype=np.float32))

    points = load_point_cloud(source)

    assert points.dtype == np.float64
    np.testing.assert_array_equal(points, np.array([[1.0, 2.0, 3.0]]))


def test_load_point_cloud_rejects_missing_points_key(tmp_path: Path) -> None:
    source = tmp_path / "invalid.npz"
    np.savez(source, depth=np.array([1]))

    with pytest.raises(ValueError, match="points_mm"):
        load_point_cloud(source)
