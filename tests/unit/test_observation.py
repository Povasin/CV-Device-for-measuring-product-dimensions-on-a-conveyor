from __future__ import annotations

import numpy as np
import pytest

from ozon_dim.measurement.observation import CaptureEvidence, ObjectObservation
from ozon_dim.pipeline import MeasurementStatus, measure_observation


def _box_touching_conveyor() -> np.ndarray:
    return np.array(
        [
            [0.0, 0.0, 0.0],
            [200.0, 0.0, 0.0],
            [0.0, 100.0, 0.0],
            [200.0, 100.0, 0.0],
            [0.0, 0.0, 50.0],
            [200.0, 0.0, 50.0],
            [0.0, 100.0, 50.0],
            [200.0, 100.0, 50.0],
        ],
        dtype=np.float64,
    )


def test_observation_measures_a_segmented_product_touching_the_conveyor() -> None:
    observation = ObjectObservation(
        event_id="event-1",
        points_mm=_box_touching_conveyor(),
        evidence=CaptureEvidence.complete({"top", "left", "right"}),
    )

    result = measure_observation(observation)

    assert result.status is MeasurementStatus.VALID
    assert result.reason is None
    assert result.dimensions_mm is not None
    np.testing.assert_allclose(np.sort(result.dimensions_mm), [50.0, 100.0, 200.0])


def test_observation_rejects_incomplete_multi_sensor_coverage() -> None:
    observation = ObjectObservation(
        event_id="event-2",
        points_mm=_box_touching_conveyor(),
        evidence=CaptureEvidence(
            required_sensor_ids=frozenset({"top", "left", "right"}),
            observed_sensor_ids=frozenset({"top"}),
            missing_profile_count=0,
            touches_roi_boundary=False,
            component_count=1,
        ),
    )

    result = measure_observation(observation)

    assert result.status is MeasurementStatus.REJECTED
    assert result.dimensions_mm is None
    assert result.reason == "missing required sensor observations: left, right"


def test_capture_evidence_rejects_a_non_string_sensor_identifier() -> None:
    with pytest.raises(ValueError, match="required_sensor_ids"):
        CaptureEvidence(
            required_sensor_ids=frozenset({"top", None}),  # type: ignore[arg-type]
            observed_sensor_ids=frozenset({"top"}),
            missing_profile_count=0,
            touches_roi_boundary=False,
            component_count=1,
        )
