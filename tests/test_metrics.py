import pytest

from pegy_tracker.calculations.metrics import cagr, eps_cagr_from_annual


def test_cagr_returns_expected_value() -> None:
    result = cagr(100.0, 121.0, 2)
    assert result is not None
    assert result == pytest.approx(0.1)


def test_cagr_invalid_inputs_return_none() -> None:
    assert cagr(100.0, 121.0, 0) is None
    assert cagr(-1.0, 121.0, 2) is None
    assert cagr(100.0, 0.0, 2) is None


def test_eps_cagr_from_annual_happy_path() -> None:
    eps = {2019: 1.0, 2024: 2.0}
    result = eps_cagr_from_annual(eps, years=5)
    assert result is not None
    assert round(result, 6) == round((2.0 ** (1 / 5)) - 1, 6)


def test_eps_cagr_from_annual_requires_start_year() -> None:
    eps = {2020: 1.0, 2024: 2.0}
    assert eps_cagr_from_annual(eps, years=5) is None
