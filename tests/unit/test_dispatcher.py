from pathlib import Path

from ozon_dim.api.dispatcher import dispatch_pending
from ozon_dim.api.outbox import MeasurementMessage, SqliteOutbox


def test_dispatcher_marks_only_successfully_sent_messages_as_delivered(tmp_path: Path) -> None:
    outbox = SqliteOutbox(tmp_path / "outbox.sqlite3")
    message = MeasurementMessage("m-1", (100.0, 200.0, 300.0), "approximate", "cal-1")
    outbox.enqueue(message)

    delivered = dispatch_pending(outbox, lambda sent: sent.measurement_id == "m-1")

    assert delivered == 1
    assert outbox.pending() == []


def test_dispatcher_keeps_message_pending_when_transport_rejects_it(tmp_path: Path) -> None:
    outbox = SqliteOutbox(tmp_path / "outbox.sqlite3")
    message = MeasurementMessage("m-1", (100.0, 200.0, 300.0), "approximate", "cal-1")
    outbox.enqueue(message)

    delivered = dispatch_pending(outbox, lambda _: False)

    assert delivered == 0
    assert outbox.pending() == [message]
