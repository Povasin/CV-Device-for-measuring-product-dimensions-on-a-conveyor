from __future__ import annotations

import numpy as np

from ozon_dim.acquisition.profiles import LaserProfile, ProfileBundle
from ozon_dim.acquisition.registration import assemble_object_observation
from ozon_dim.pipeline import MeasurementStatus, measure_observation


def _dense_cube() -> np.ndarray:
    values = np.array([0.0, 10.0, 20.0])
    x, y, z = np.meshgrid(values, values, values, indexing="ij")
    return np.column_stack((x.ravel(), y.ravel(), z.ravel()))


def test_profile_bundle_registers_and_measures_one_complete_product() -> None:
    profile = LaserProfile(
        sensor_id="top",
        profile_index=1,
        captured_at_ns=10,
        encoder_count=110,
        points_sensor_mm=_dense_cube(),
        valid_mask=np.ones(27, dtype=bool),
        intensity=None,
        calibration_id="cal-1",
    )
    bundle = ProfileBundle.from_profiles("event-1", frozenset({"top"}), (profile,))

    observation = assemble_object_observation(
        bundle,
        sensor_to_conveyor={"top": np.eye(4)},
        reference_encoder_count=100,
        mm_per_encoder_count=0.05,
        max_neighbor_distance_mm=18.0,
        min_component_points=4,
    )
    result = measure_observation(observation)

    assert result.status is MeasurementStatus.VALID
    assert result.dimensions_mm is not None
    np.testing.assert_allclose(np.sort(result.dimensions_mm), [20.0, 20.0, 20.0])


def test_incomplete_bundle_becomes_a_rejected_measurement_instead_of_a_partial_box() -> None:
    profile = LaserProfile(
        sensor_id="top",
        profile_index=1,
        captured_at_ns=10,
        encoder_count=100,
        points_sensor_mm=_dense_cube(),
        valid_mask=np.ones(27, dtype=bool),
        intensity=None,
        calibration_id="cal-1",
    )
    bundle = ProfileBundle.from_profiles("event-2", frozenset({"top", "left", "right"}), (profile,))

    observation = assemble_object_observation(
        bundle,
        sensor_to_conveyor={"top": np.eye(4)},
        reference_encoder_count=100,
        mm_per_encoder_count=0.05,
        max_neighbor_distance_mm=18.0,
        min_component_points=4,
    )
    result = measure_observation(observation)

    assert result.status is MeasurementStatus.REJECTED
    assert result.reason == "missing required sensor observations: left, right"
