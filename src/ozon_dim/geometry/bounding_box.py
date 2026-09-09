"""Explicitly labelled oriented bounding-box baselines."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import open3d as o3d


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """An oriented bounding box represented in millimetres."""

    center: npt.NDArray[np.float64]
    rotation: npt.NDArray[np.float64]
    extents: npt.NDArray[np.float64]
    algorithm: str

    def __post_init__(self) -> None:
        for field_name, value, shape in (
            ("center", self.center, (3,)),
            ("rotation", self.rotation, (3, 3)),
            ("extents", self.extents, (3,)),
        ):
            array = np.asarray(value, dtype=np.float64)
            if array.shape != shape or not np.all(np.isfinite(array)):
                raise ValueError(f"{field_name} must be finite with shape {shape}")
            array = np.array(array, copy=True)
            array.setflags(write=False)
            object.__setattr__(self, field_name, array)
        if np.any(self.extents <= 0.0):
            raise ValueError("extents must be positive")


def approximate_oriented_bounding_box(points: npt.NDArray[np.float64]) -> BoundingBox:
    """Return Open3D's face-aligned minimum-volume approximation.

    This is a baseline only. It must not be presented as a globally exact MVBB.
    """
    points_array = np.asarray(points, dtype=np.float64)
    if points_array.ndim != 2 or points_array.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")
    if not np.all(np.isfinite(points_array)):
        raise ValueError("points must contain only finite values")
    if points_array.shape[0] < 4:
        raise ValueError("points must contain at least four points")
    if np.linalg.matrix_rank(points_array - points_array.mean(axis=0)) < 3:
        raise ValueError("points must span three dimensions")

    # Open3D's legacy Vector3dVector constructor requires a writeable NumPy buffer.
    # ObjectObservation intentionally owns an immutable validated copy, so isolate the
    # backend boundary with a writable copy rather than weakening that contract.
    point_cloud = o3d.geometry.PointCloud(
        o3d.utility.Vector3dVector(np.array(points_array, copy=True))
    )
    box = point_cloud.get_minimal_oriented_bounding_box()
    return BoundingBox(
        center=np.asarray(box.center, dtype=np.float64),
        rotation=np.asarray(box.R, dtype=np.float64),
        extents=np.asarray(box.extent, dtype=np.float64),
        algorithm="open3d-face-aligned-approx",
    )
