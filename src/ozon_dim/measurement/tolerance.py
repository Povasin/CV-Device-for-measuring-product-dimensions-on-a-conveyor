"""Tolerance rule from the test assignment."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def tolerance_mm(dimension_mm: float) -> float:
    """Return max(5% of a dimension, 5 mm)."""
    value = float(dimension_mm)
    if not np.isfinite(value):
        raise ValueError("dimension_mm must be finite")
    if value < 0:
        raise ValueError("dimension_mm must be non-negative")
    return max(0.05 * value, 5.0)


def dimensions_within_tolerance(
    measured_mm: npt.NDArray[np.float64], reference_mm: npt.NDArray[np.float64]
) -> bool:
    """Check every dimension against the assignment tolerance independently."""
    measured = np.asarray(measured_mm, dtype=np.float64)
    reference = np.asarray(reference_mm, dtype=np.float64)
    if measured.shape != (3,) or reference.shape != (3,):
        raise ValueError("measured_mm and reference_mm must have shape (3,)")
    if not np.all(np.isfinite(measured)) or not np.all(np.isfinite(reference)):
        raise ValueError("dimensions must be finite")
    if measured.shape != reference.shape:
        raise ValueError("measured_mm and reference_mm must have equal shapes")
    if np.any(measured < 0) or np.any(reference < 0):
        raise ValueError("dimensions must be non-negative")
    allowed_error = np.maximum(0.05 * reference, 5.0)
    return bool(np.all(np.abs(measured - reference) <= allowed_error))
