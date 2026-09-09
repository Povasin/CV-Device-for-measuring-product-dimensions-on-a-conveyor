"""Rigid coordinate transforms for point clouds expressed in millimetres."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def validate_rigid_transform(transform: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """Validate and return a finite, right-handed rigid homogeneous transform."""
    transform_array = np.asarray(transform, dtype=np.float64)
    if transform_array.shape != (4, 4):
        raise ValueError("transform must have shape (4, 4)")
    if not np.all(np.isfinite(transform_array)):
        raise ValueError("transform must contain only finite values")
    if not np.allclose(transform_array[3], [0.0, 0.0, 0.0, 1.0]):
        raise ValueError("transform must have a homogeneous final row")
    rotation = transform_array[:3, :3]
    if not np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-8):
        raise ValueError("transform rotation must be orthonormal")
    if not np.isclose(np.linalg.det(rotation), 1.0, atol=1e-8):
        raise ValueError("transform rotation must have determinant +1")
    return transform_array


def transform_points(
    points: npt.NDArray[np.float64], transform: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    """Apply a homogeneous 4×4 transform to N three-dimensional points."""
    points_array = np.asarray(points, dtype=np.float64)
    if points_array.ndim != 2 or points_array.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")
    if not np.all(np.isfinite(points_array)):
        raise ValueError("points must contain only finite values")
    transform_array = validate_rigid_transform(transform)

    homogeneous_points = np.column_stack(
        (points_array, np.ones(points_array.shape[0], dtype=np.float64))
    )
    return (homogeneous_points @ transform_array.T)[:, :3]
