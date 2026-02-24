from __future__ import annotations
from typing import List, Dict, Optional

from pegy_tracker.domain.models import FundamentalsSnapshot, MetricResult
from pegy_tracker.calculations.metrics import eps_cagr_from_annual
from pegy_tracker.calculations.validation import validate_positive, cap_outliers


class PegyCalculator:
    """
    PEGY = (P/E) / (EPS growth % + dividend yield %)
    Growth is EPS CAGR by default (5y) but can be swapped later for forward estimates.
    """

    def __init__(
        self,
        eps_cagr_years: int = 5,
        growth_clip: tuple[float, float] = (0.0, 0.5),      # 0%..50% per year
        div_yield_clip: tuple[float, float] = (0.0, 0.2),   # 0%..20%
        denom_floor_pct: float = 1.0,                       # 1% minimum to avoid crazy ratios
    ):
        self.eps_cagr_years = eps_cagr_years
        self.growth_clip = growth_clip
        self.div_yield_clip = div_yield_clip
        self.denom_floor_pct = denom_floor_pct

    def compute(self, snap: FundamentalsSnapshot) -> MetricResult:
        flags: List[str] = []
        metrics: Dict[str, float] = {}

        pe = snap.earnings.pe_ttm
        if pe is None and snap.earnings.eps_ttm is not None:
            # derive P/E if needed
            if snap.earnings.eps_ttm != 0:
                pe = snap.price.close / snap.earnings.eps_ttm

        if not validate_positive(pe, "pe", flags):
            return MetricResult(snap.instrument, snap.asof, metrics={}, flags=flags)

        growth = eps_cagr_from_annual(snap.earnings.eps_annual, years=self.eps_cagr_years)
        if growth is None:
            flags.append("missing:growth")
            return MetricResult(snap.instrument, snap.asof, metrics={}, flags=flags)

        div_yield = snap.dividends.dividend_yield
        if div_yield is None:
            flags.append("missing:div_yield")
            return MetricResult(snap.instrument, snap.asof, metrics={}, flags=flags)

        # clip outliers
        growth = cap_outliers(growth, self.growth_clip[0], self.growth_clip[1], "growth", flags)
        div_yield = cap_outliers(div_yield, self.div_yield_clip[0], self.div_yield_clip[1], "div_yield", flags)

        growth_pct = growth * 100.0
        div_yield_pct = div_yield * 100.0
        denom = growth_pct + div_yield_pct

        if denom < self.denom_floor_pct:
            flags.append("denom_too_small")
            return MetricResult(snap.instrument, snap.asof, metrics={}, flags=flags)

        pegy = pe / denom

        metrics["pe"] = float(pe)
        metrics[f"eps_cagr_{self.eps_cagr_years}y"] = float(growth)
        metrics["div_yield"] = float(div_yield)
        metrics["pegy"] = float(pegy)

        return MetricResult(snap.instrument, snap.asof, metrics=metrics, flags=flags)