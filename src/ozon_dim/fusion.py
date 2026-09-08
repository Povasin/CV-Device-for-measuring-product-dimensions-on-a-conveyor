"""Fusion of point clouds already calibrated to the conveyor coordinate system."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ozon_dim.geometry.transforms import transform_points


def fuse_point_clouds(
    point_clouds: list[npt.NDArray[np.float64]], transforms: list[npt.NDArray[np.float64]]
) -> npt.NDArray[np.float64]:
    """Transform and concatenate clouds from synchronized sensors.

    Temporal synchronization and calibration estimation are hardware-side concerns;
    this function only applies supplied rigid transforms.
    """
    if len(point_clouds) != len(transforms):
        raise ValueError("point_clouds and transforms must have the same length")
    if not point_clouds:
        return np.empty((0, 3), dtype=np.float64)
    return np.vstack([transform_points(points, transform) for points, transform in zip(point_clouds, transforms)])
