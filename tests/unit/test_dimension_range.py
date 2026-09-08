import numpy as np

from ozon_dim.measurement.validation import dimensions_within_operating_range


def test_dimensions_within_assignment_operating_range() -> None:
    assert dimensions_within_operating_range(np.array([400.0, 300.0, 10.0])) is True
    assert dimensions_within_operating_range(np.array([401.0, 300.0, 10.0])) is False
