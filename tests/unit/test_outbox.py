from pathlib import Path

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
