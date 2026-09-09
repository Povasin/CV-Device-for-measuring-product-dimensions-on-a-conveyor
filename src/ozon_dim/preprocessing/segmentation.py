"""Reject multiple products and discard isolated noise before OBB estimation."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
import open3d as o3d


class InsufficientObjectComponentError(ValueError):
    """Raised when no connected foreground component has enough support."""


class MultipleObjectComponentsError(ValueError):
    """Raised when an event contains more than one supported object component."""


def select_single_object_points(
    points_mm: npt.NDArray[np.float64],
    max_neighbor_distance_mm: float,
    min_component_points: int,
) -> npt.NDArray[np.float64]:
    """Keep exactly one DBSCAN component and treat smaller components as noise.

    This is a deterministic baseline for already foreground-segmented snapshot data.
    The radius and minimum support must be validated on recorded production profiles;
    this function deliberately rejects ambiguous events instead of merging products.
    """
    points = np.asarray(points_mm, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points_mm must have shape (N, 3)")
    if not np.all(np.isfinite(points)):
        raise ValueError("points_mm must contain only finite values")
    distance = float(max_neighbor_distance_mm)
    if not np.isfinite(distance) or distance <= 0.0:
        raise ValueError("max_neighbor_distance_mm must be finite and positive")
    if min_component_points < 2:
        raise ValueError("min_component_points must be at least two")
    if len(points) < min_component_points:
        raise InsufficientObjectComponentError("not enough points for an object component")

    cloud = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
    labels = np.asarray(
        cloud.cluster_dbscan(eps=distance, min_points=min_component_points, print_progress=False),
        dtype=np.int64,
    )
    component_labels = sorted(int(label) for label in np.unique(labels) if label >= 0)
    if not component_labels:
        raise InsufficientObjectComponentError("no supported object component was found")
    if len(component_labels) != 1:
        raise MultipleObjectComponentsError(
            f"multiple object components found: {len(component_labels)}"
        )
    return np.array(points[labels == component_labels[0]], copy=True)
