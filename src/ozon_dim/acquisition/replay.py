"""Offline frame replay without a camera SDK dependency."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import numpy.typing as npt


def load_point_cloud(path: Path) -> npt.NDArray[np.float64]:
    """Load a calibrated point cloud stored under the ``points_mm`` NPZ key."""
    with np.load(path) as frame:
        if "points_mm" not in frame:
            raise ValueError("NPZ frame must contain a points_mm array")
        points = np.asarray(frame["points_mm"], dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points_mm must have shape (N, 3)")
    return points
