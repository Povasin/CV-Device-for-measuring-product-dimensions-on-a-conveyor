"""Run the synthetic regression benchmark."""

from ozon_dim.benchmark import run_synthetic_benchmark

if __name__ == "__main__":
    report = run_synthetic_benchmark([(10.0, 10.0, 10.0), (200.0, 100.0, 50.0), (400.0, 300.0, 300.0)])
    print(f"sample_count={report.sample_count}")
    print(f"max_absolute_error_mm={report.max_absolute_error_mm}")
    print(f"within_assignment_tolerance={report.within_assignment_tolerance}")
