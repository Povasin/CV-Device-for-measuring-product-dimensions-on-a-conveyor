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


def approximate_oriented_bounding_box(points: npt.NDArray[np.float64]) -> BoundingBox:
    """Return Open3D's face-aligned minimum-volume approximation.

    This is a baseline only. It must not be presented as a globally exact MVBB.
    """
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")
    if points.shape[0] < 4:
        raise ValueError("points must contain at least four points")

    point_cloud = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
    box = point_cloud.get_minimal_oriented_bounding_box()
    return BoundingBox(
        center=np.asarray(box.center, dtype=np.float64),
        rotation=np.asarray(box.R, dtype=np.float64),
        extents=np.asarray(box.extent, dtype=np.float64),
        algorithm="open3d-face-aligned-approx",
    )
