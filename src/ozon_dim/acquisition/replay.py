"""Offline frame replay without a camera SDK dependency."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import numpy.typing as npt

from ozon_dim.acquisition.profiles import LaserProfile


def load_point_cloud(path: Path) -> npt.NDArray[np.float64]:
    """Load a calibrated point cloud stored under the ``points_mm`` NPZ key."""
    with np.load(path) as frame:
        if "points_mm" not in frame:
            raise ValueError("NPZ frame must contain a points_mm array")
        points = np.asarray(frame["points_mm"], dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points_mm must have shape (N, 3)")
    return points


def load_laser_profile(path: Path) -> LaserProfile:
    """Load a recorded line profile into the same contract used by a live adapter."""
    required_keys = {
        "sensor_id",
        "profile_index",
        "captured_at_ns",
        "encoder_count",
        "points_sensor_mm",
        "valid_mask",
        "calibration_id",
    }
    with np.load(path) as frame:
        missing_keys = sorted(required_keys - set(frame.files))
        if missing_keys:
            raise ValueError(f"profile NPZ is missing keys: {', '.join(missing_keys)}")
        intensity = (
            np.asarray(frame["intensity"], dtype=np.float64) if "intensity" in frame.files else None
        )
        return LaserProfile(
            sensor_id=str(frame["sensor_id"].item()),
            profile_index=int(frame["profile_index"].item()),
            captured_at_ns=int(frame["captured_at_ns"].item()),
            encoder_count=int(frame["encoder_count"].item()),
            points_sensor_mm=np.asarray(frame["points_sensor_mm"], dtype=np.float64),
            valid_mask=np.asarray(frame["valid_mask"], dtype=np.bool_),
            intensity=intensity,
            calibration_id=str(frame["calibration_id"].item()),
        )
