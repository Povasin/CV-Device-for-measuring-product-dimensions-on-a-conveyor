"""Validated representation of an externally measured sensor calibration."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ozon_dim.geometry.transforms import validate_rigid_transform


@dataclass(frozen=True, slots=True)
class Calibration:
    """Rigid sensor-to-conveyor transform and its traceable identifier."""

    calibration_id: str
    transform: npt.NDArray[np.float64]

    def __post_init__(self) -> None:
        if not self.calibration_id:
            raise ValueError("calibration_id must not be empty")
        transform = np.array(validate_rigid_transform(self.transform), copy=True)
        transform.setflags(write=False)
        object.__setattr__(self, "transform", transform)
