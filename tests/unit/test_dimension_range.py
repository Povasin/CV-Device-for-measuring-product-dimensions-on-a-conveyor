import numpy as np
import pytest

from ozon_dim.measurement.validation import dimensions_within_operating_range


def test_dimensions_within_assignment_operating_range() -> None:
    assert dimensions_within_operating_range(np.array([400.0, 300.0, 10.0])) is True
    assert dimensions_within_operating_range(np.array([401.0, 300.0, 10.0])) is False


def test_operating_range_rejects_non_finite_dimensions() -> None:
    with pytest.raises(ValueError, match="finite"):
        dimensions_within_operating_range(np.array([10.0, 10.0, float("inf")]))
