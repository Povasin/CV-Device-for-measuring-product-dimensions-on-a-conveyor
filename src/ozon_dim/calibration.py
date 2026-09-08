"""Validated representation of an externally measured sensor calibration."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True, slots=True)
class Calibration:
    """Rigid sensor-to-conveyor transform and its traceable identifier."""

    calibration_id: str
    transform: npt.NDArray[np.float64]

    def __post_init__(self) -> None:
        if not self.calibration_id:
            raise ValueError("calibration_id must not be empty")
        if self.transform.shape != (4, 4):
            raise ValueError("transform must have shape (4, 4)")
        if not np.allclose(self.transform[3], [0.0, 0.0, 0.0, 1.0]):
            raise ValueError("transform must have a homogeneous final row")
        rotation = self.transform[:3, :3]
        if not np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-8):
            raise ValueError("transform rotation must be orthonormal")
        if not np.isclose(np.linalg.det(rotation), 1.0, atol=1e-8):
            raise ValueError("transform rotation must have determinant +1")
