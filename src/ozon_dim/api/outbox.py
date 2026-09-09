"""Durable, idempotent outbox for WMS measurement events."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from math import isfinite
from pathlib import Path


def _require_non_empty_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


@dataclass(frozen=True, slots=True)
class MeasurementMessage:
    """Measurement payload with a caller-provided idempotency key."""

    measurement_id: str
    dimensions_mm: tuple[float, float, float]
    algorithm: str
    calibration_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "measurement_id", _require_non_empty_text(self.measurement_id, "measurement_id")
        )
        object.__setattr__(self, "algorithm", _require_non_empty_text(self.algorithm, "algorithm"))
        object.__setattr__(
            self, "calibration_id", _require_non_empty_text(self.calibration_id, "calibration_id")
        )
        if len(self.dimensions_mm) != 3:
            raise ValueError("dimensions_mm must contain exactly three values")
        dimensions = tuple(float(value) for value in self.dimensions_mm)
        if not all(isfinite(value) and value > 0 for value in dimensions):
            raise ValueError("dimensions_mm must contain finite positive values")
        object.__setattr__(self, "dimensions_mm", dimensions)


class SqliteOutbox:
    """Persist messages locally before a WMS transport acknowledges delivery."""

    def __init__(self, path: Path) -> None:
        self._connection = sqlite3.connect(path)
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS outbox (
                measurement_id TEXT PRIMARY KEY CHECK(length(trim(measurement_id)) > 0),
                length_mm REAL NOT NULL CHECK(length_mm > 0),
                width_mm REAL NOT NULL CHECK(width_mm > 0),
                height_mm REAL NOT NULL CHECK(height_mm > 0),
                algorithm TEXT NOT NULL CHECK(length(trim(algorithm)) > 0),
                calibration_id TEXT NOT NULL CHECK(length(trim(calibration_id)) > 0),
                delivered INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        self._connection.commit()

    def enqueue(self, message: MeasurementMessage) -> bool:
        """Store a message once; return false only for an existing idempotency key."""
        try:
            self._connection.execute(
                """
                INSERT INTO outbox
                (measurement_id, length_mm, width_mm, height_mm, algorithm, calibration_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    message.measurement_id,
                    *message.dimensions_mm,
                    message.algorithm,
                    message.calibration_id,
                ),
            )
            self._connection.commit()
        except sqlite3.IntegrityError:
            self._connection.rollback()
            existing = self._connection.execute(
                "SELECT 1 FROM outbox WHERE measurement_id = ?", (message.measurement_id,)
            ).fetchone()
            if existing is not None:
                return False
            raise
        return True

    def pending(self) -> list[MeasurementMessage]:
        """Return messages whose transport acknowledgement has not been recorded."""
        rows = self._connection.execute(
            """
            SELECT measurement_id, length_mm, width_mm, height_mm, algorithm, calibration_id
            FROM outbox WHERE delivered = 0 ORDER BY rowid
            """
        ).fetchall()
        return [
            MeasurementMessage(
                measurement_id=row[0],
                dimensions_mm=(row[1], row[2], row[3]),
                algorithm=row[4],
                calibration_id=row[5],
            )
            for row in rows
        ]

    def mark_delivered(self, measurement_id: str) -> None:
        """Record successful downstream acknowledgement."""
        self._connection.execute(
            "UPDATE outbox SET delivered = 1 WHERE measurement_id = ?", (measurement_id,)
        )
        self._connection.commit()
