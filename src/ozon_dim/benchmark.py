"""Synthetic benchmark for deterministic pipeline regression checks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ozon_dim.demo import synthetic_product_cloud
from ozon_dim.measurement.tolerance import dimensions_within_tolerance
from ozon_dim.pipeline import measure_product


@dataclass(frozen=True, slots=True)
class BenchmarkReport:
    """Aggregate results for an explicitly synthetic test corpus."""

    sample_count: int
    max_absolute_error_mm: float
    within_assignment_tolerance: bool


def run_synthetic_benchmark(cases_mm: list[tuple[float, float, float]]) -> BenchmarkReport:
    """Measure axis-aligned boxes and report deterministic regression metrics.

    This validates software mechanics only; it is not a measurement-accuracy claim
    for a physical camera/conveyor system.
    """
    if not cases_mm:
        raise ValueError("cases_mm must not be empty")
    absolute_errors: list[np.ndarray] = []
    passed: list[bool] = []
    for dimensions in cases_mm:
        result = measure_product(synthetic_product_cloud(dimensions))
        reference = np.sort(np.asarray(dimensions, dtype=np.float64))
        measured = np.sort(result.dimensions_mm)
        absolute_errors.append(np.abs(measured - reference))
        passed.append(dimensions_within_tolerance(measured, reference))
    return BenchmarkReport(
        sample_count=len(cases_mm),
        max_absolute_error_mm=float(np.max(np.vstack(absolute_errors))),
        within_assignment_tolerance=all(passed),
    )
