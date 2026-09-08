"""Rigid coordinate transforms for point clouds expressed in millimetres."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def transform_points(
    points: npt.NDArray[np.float64], transform: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    """Apply a homogeneous 4×4 transform to N three-dimensional points."""
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")
    if transform.shape != (4, 4):
        raise ValueError("transform must have shape (4, 4)")

    homogeneous_points = np.column_stack((points, np.ones(points.shape[0], dtype=np.float64)))
    return (homogeneous_points @ transform.T)[:, :3]
