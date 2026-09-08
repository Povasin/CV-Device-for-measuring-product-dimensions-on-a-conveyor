"""Tolerance rule from the test assignment."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def tolerance_mm(dimension_mm: float) -> float:
    """Return max(5% of a dimension, 5 mm)."""
    if dimension_mm < 0:
        raise ValueError("dimension_mm must be non-negative")
    return max(0.05 * dimension_mm, 5.0)


def dimensions_within_tolerance(
    measured_mm: npt.NDArray[np.float64], reference_mm: npt.NDArray[np.float64]
) -> bool:
    """Check every dimension against the assignment tolerance independently."""
    if measured_mm.shape != reference_mm.shape:
        raise ValueError("measured_mm and reference_mm must have equal shapes")
    if np.any(measured_mm < 0) or np.any(reference_mm < 0):
        raise ValueError("dimensions must be non-negative")
    allowed_error = np.maximum(0.05 * reference_mm, 5.0)
    return bool(np.all(np.abs(measured_mm - reference_mm) <= allowed_error))
