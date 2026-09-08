from ozon_dim.api.outbox import MeasurementMessage
from ozon_dim.api.payload import measurement_payload


def test_measurement_payload_keeps_units_and_traceability_fields() -> None:
    message = MeasurementMessage("m-1", (100.0, 200.0, 300.0), "approximate", "cal-1")

    payload = measurement_payload(message)

    assert payload == {
        "measurement_id": "m-1",
        "dimensions_mm": [100.0, 200.0, 300.0],
        "algorithm": "approximate",
        "calibration_id": "cal-1",
    }
