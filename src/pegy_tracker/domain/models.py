from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, List


@dataclass(frozen=True)
class InstrumentId:
    """Provider-agnostic identifier of a tradable equity."""
    symbol: str           # e.g. "EQNR.OL"
    mic: str              # e.g. "XOSL"
    isin: Optional[str] = None
    name: Optional[str] = None
    currency: Optional[str] = None


@dataclass(frozen=True)
class PricePoint:
    asof: date
    close: float
    currency: str


@dataclass(frozen=True)
class DividendInfo:
    """Dividend yield is simplest, but keep raw DPS if possible."""
    asof: date
    ttm_dividend_per_share: Optional[float]  # in currency
    dividend_yield: Optional[float]          # decimal, e.g. 0.042


@dataclass(frozen=True)
class EarningsInfo:
    """TTM and annual series if available."""
    asof: date
    eps_ttm: Optional[float]
    pe_ttm: Optional[float]
    # annual diluted EPS history: {year: eps}
    eps_annual: Dict[int, float]


@dataclass(frozen=True)
class FundamentalsSnapshot:
    """All inputs needed for most value metrics."""
    instrument: InstrumentId
    asof: date
    price: PricePoint
    earnings: EarningsInfo
    dividends: DividendInfo
    sector: Optional[str] = None           # normalized sector label
    industry: Optional[str] = None
    extra: Optional[dict] = None           # provider-specific raw (optional)


@dataclass(frozen=True)
class MetricResult:
    instrument: InstrumentId
    asof: date
    metrics: Dict[str, float]              # e.g. {"pegy": 0.83, "eps_cagr_5y": 0.12}
    flags: List[str]                       # validation notes / warnings