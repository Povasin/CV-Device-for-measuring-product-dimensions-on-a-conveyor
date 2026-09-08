"""Explicit, transport-neutral representation of a WMS measurement event."""

from __future__ import annotations

from typing import TypedDict

from ozon_dim.api.outbox import MeasurementMessage


class WmsMeasurementPayload(TypedDict):
    """JSON-compatible WMS payload with dimensions always expressed in millimetres."""

    measurement_id: str
    dimensions_mm: list[float]
    algorithm: str
    calibration_id: str


def measurement_payload(message: MeasurementMessage) -> WmsMeasurementPayload:
    """Convert a durable measurement event into an explicit JSON-compatible payload."""
    return {
        "measurement_id": message.measurement_id,
        "dimensions_mm": list(message.dimensions_mm),
        "algorithm": message.algorithm,
        "calibration_id": message.calibration_id,
    }
