import pytest

from ozon_dim.benchmark import run_synthetic_benchmark


def test_synthetic_benchmark_reports_zero_error_for_axis_aligned_boxes() -> None:
    report = run_synthetic_benchmark([(10.0, 10.0, 10.0), (400.0, 300.0, 300.0)])

    assert report.sample_count == 2
    assert report.max_absolute_error_mm == pytest.approx(0.0)
    assert report.within_assignment_tolerance is True
