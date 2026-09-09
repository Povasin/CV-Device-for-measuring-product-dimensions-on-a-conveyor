from pathlib import Path

import pytest

from ozon_dim.api.outbox import MeasurementMessage, SqliteOutbox


def test_outbox_deduplicates_same_measurement_id(tmp_path: Path) -> None:
    outbox = SqliteOutbox(tmp_path / "outbox.sqlite3")
    message = MeasurementMessage("m-1", (100.0, 200.0, 300.0), "approximate", "cal-1")

    assert outbox.enqueue(message) is True
    assert outbox.enqueue(message) is False
    assert outbox.pending() == [message]


def test_outbox_marks_message_delivered(tmp_path: Path) -> None:
    outbox = SqliteOutbox(tmp_path / "outbox.sqlite3")
    message = MeasurementMessage("m-1", (100.0, 200.0, 300.0), "approximate", "cal-1")
    outbox.enqueue(message)

    outbox.mark_delivered("m-1")

    assert outbox.pending() == []


def test_outbox_returns_false_only_for_a_duplicate_measurement_id(tmp_path: Path) -> None:
    outbox = SqliteOutbox(tmp_path / "outbox.sqlite")
    message = MeasurementMessage("m-1", (100.0, 200.0, 300.0), "approximate", "cal-1")

    assert outbox.enqueue(message) is True
    assert outbox.enqueue(message) is False


@pytest.mark.parametrize(
    ("measurement_id", "dimensions_mm", "algorithm", "calibration_id"),
    [
        ("", (100.0, 200.0, 300.0), "approximate", "cal-1"),
        ("m-1", (-1.0, 200.0, 300.0), "approximate", "cal-1"),
        ("m-1", (100.0, float("inf"), 300.0), "approximate", "cal-1"),
        (None, (100.0, 200.0, 300.0), "approximate", "cal-1"),
    ],
)
def test_measurement_message_rejects_invalid_delivery_data(
    measurement_id: str,
    dimensions_mm: tuple[float, float, float],
    algorithm: str,
    calibration_id: str,
) -> None:
    with pytest.raises(ValueError):
        MeasurementMessage(measurement_id, dimensions_mm, algorithm, calibration_id)
