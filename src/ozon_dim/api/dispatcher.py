"""Delivery loop for the durable WMS outbox."""

from __future__ import annotations

from collections.abc import Callable

from ozon_dim.api.outbox import MeasurementMessage, SqliteOutbox


def dispatch_pending(outbox: SqliteOutbox, send: Callable[[MeasurementMessage], bool]) -> int:
    """Send pending messages and persist acknowledgements one by one.

    ``send`` must return true only after the downstream WMS accepts the event.
    Exceptions propagate so an external worker can apply its own retry policy;
    unacknowledged messages remain durable in the outbox.
    """
    delivered = 0
    for message in outbox.pending():
        if send(message):
            outbox.mark_delivered(message.measurement_id)
            delivered += 1
    return delivered
