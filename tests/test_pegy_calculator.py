from datetime import date

from pegy_tracker.calculations.pegy import PegyCalculator
from pegy_tracker.domain.models import (
    DividendInfo,
    EarningsInfo,
    FundamentalsSnapshot,
    InstrumentId,
    PricePoint,
)


def make_snapshot(*, pe_ttm: float | None, eps_ttm: float | None, growth_start: float, growth_end: float, div_yield: float | None) -> FundamentalsSnapshot:
    asof = date(2024, 1, 1)
    return FundamentalsSnapshot(
        instrument=InstrumentId(symbol="EQNR.OL", mic="XOSL"),
        asof=asof,
        price=PricePoint(asof=asof, close=100.0, currency="NOK"),
        earnings=EarningsInfo(
            asof=asof,
            eps_ttm=eps_ttm,
            pe_ttm=pe_ttm,
            eps_annual={2019: growth_start, 2024: growth_end},
        ),
        dividends=DividendInfo(asof=asof, ttm_dividend_per_share=1.0, dividend_yield=div_yield),
    )


def test_compute_returns_metrics_when_inputs_are_valid() -> None:
    calc = PegyCalculator()
    snap = make_snapshot(pe_ttm=15.0, eps_ttm=10.0, growth_start=1.0, growth_end=2.0, div_yield=0.05)

    result = calc.compute(snap)

    assert result.flags == []
    assert result.metrics["pe"] == 15.0
    assert "pegy" in result.metrics


def test_compute_derives_pe_from_price_and_eps_ttm() -> None:
    calc = PegyCalculator()
    snap = make_snapshot(pe_ttm=None, eps_ttm=5.0, growth_start=1.0, growth_end=2.0, div_yield=0.05)

    result = calc.compute(snap)

    assert result.metrics["pe"] == 20.0


def test_compute_returns_flags_for_missing_fields() -> None:
    calc = PegyCalculator()
    snap = make_snapshot(pe_ttm=10.0, eps_ttm=5.0, growth_start=1.0, growth_end=2.0, div_yield=None)

    result = calc.compute(snap)

    assert result.metrics == {}
    assert "missing:div_yield" in result.flags
