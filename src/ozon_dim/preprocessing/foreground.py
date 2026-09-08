"""Conveyor-background removal for calibrated point clouds."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def points_above_conveyor(
    points: npt.NDArray[np.float64], conveyor_z_mm: float = 0.0, min_height_mm: float = 2.0
) -> npt.NDArray[np.float64]:
    """Return points more than ``min_height_mm`` above the conveyor plane.

    Inputs must already be expressed in the conveyor coordinate system.
    """
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")
    if min_height_mm < 0:
        raise ValueError("min_height_mm must be non-negative")
    return points[points[:, 2] > conveyor_z_mm + min_height_mm]
