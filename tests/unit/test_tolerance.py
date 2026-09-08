import numpy as np
import pytest

from ozon_dim.measurement.tolerance import dimensions_within_tolerance, tolerance_mm


@pytest.mark.parametrize(
    ("dimension_mm", "expected_mm"),
    [(10.0, 5.0), (100.0, 5.0), (200.0, 10.0)],
)
def test_tolerance_is_maximum_of_five_percent_and_five_mm(
    dimension_mm: float, expected_mm: float
) -> None:
    assert tolerance_mm(dimension_mm) == expected_mm


def test_all_dimensions_must_satisfy_the_tolerance() -> None:
    measured = np.array([100.0, 200.0, 300.0], dtype=np.float64)
    reference = np.array([104.0, 211.0, 315.0], dtype=np.float64)

    assert not dimensions_within_tolerance(measured, reference)


def test_negative_dimension_is_invalid() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        tolerance_mm(-1.0)
