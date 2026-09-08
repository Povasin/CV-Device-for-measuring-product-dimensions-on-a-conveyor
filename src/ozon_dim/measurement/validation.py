"""Validation against the explicit operating-size range of variant 1."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def dimensions_within_operating_range(dimensions_mm: npt.NDArray[np.float64]) -> bool:
    """Return whether sorted dimensions fit 10x10x10 through 400x300x300 mm."""
    if dimensions_mm.shape != (3,):
        raise ValueError("dimensions_mm must have shape (3,)")
    ordered = np.sort(dimensions_mm)
    lower = np.array([10.0, 10.0, 10.0])
    upper = np.array([300.0, 300.0, 400.0])
    return bool(np.all(ordered >= lower) and np.all(ordered <= upper))
