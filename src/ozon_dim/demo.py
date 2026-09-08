"""Reproducible synthetic demo for the offline pipeline."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def synthetic_product_cloud(dimensions_mm: tuple[float, float, float]) -> npt.NDArray[np.float64]:
    """Create box corners above the conveyor plane for a deterministic demo."""
    if any(dimension <= 0 for dimension in dimensions_mm):
        raise ValueError("all dimensions must be positive")
    length, width, height = dimensions_mm
    x_values = (0.0, length)
    y_values = (0.0, width)
    z_values = (10.0, 10.0 + height)
    return np.array(
        [[x, y, z] for x in x_values for y in y_values for z in z_values], dtype=np.float64
    )
