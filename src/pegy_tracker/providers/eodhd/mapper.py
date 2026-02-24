from __future__ import annotations
from datetime import date
from typing import Any, Dict, Optional

from pegy_tracker.domain.models import (
    InstrumentId, PricePoint, DividendInfo, EarningsInfo, FundamentalsSnapshot
)

def _to_float(x) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None

def _extract_eps_annual(fundamentals: Dict[str, Any]) -> Dict[int, float]:
    """
    Provider schemas vary. Keep this robust and evolve with real payloads.
    Try common locations for annual diluted EPS.
    """
    out: Dict[int, float] = {}
    financials = fundamentals.get("Financials", {}) or {}
    annual = financials.get("Annual", {}) or {}
    income_stmt = annual.get("Income_Statement", {}) or {}

    # Some providers use year keys -> dict
    for year_str, row in income_stmt.items():
        try:
            year = int(year_str)
        except Exception:
            continue
        if not isinstance(row, dict):
            continue

        eps = row.get("dilutedEPS") or row.get("epsDiluted") or row.get("EPS_Diluted")
        eps = _to_float(eps)
        if eps is not None:
            out[year] = eps

    return out

def map_eodhd_to_snapshot(
    symbol: str,
    mic: str,
    fundamentals: Dict[str, Any],
    latest_bar: Dict[str, Any],
    asof: Optional[date] = None,
) -> FundamentalsSnapshot:
    asof = asof or date.today()

    gen = fundamentals.get("General", {}) or {}
    highlights = fundamentals.get("Highlights", {}) or {}
    # Sometimes there is a "Technicals" or "Valuation"; keep optional.
    valuation = fundamentals.get("Valuation", {}) or {}

    name = gen.get("Name")
    isin = gen.get("ISIN")
    currency = gen.get("CurrencyCode") or gen.get("Currency") or highlights.get("Currency")
    sector = gen.get("Sector")
    industry = gen.get("Industry")

    close = _to_float(latest_bar.get("close") or latest_bar.get("Close"))
    if close is None:
        # fallback: some payloads include "Highlights" -> "Price"
        close = _to_float(highlights.get("MarketCapitalization"))  # not ideal; you’ll adjust
        # better to raise and handle upstream:
        raise ValueError(f"Missing latest close for {symbol}")

    instrument = InstrumentId(symbol=symbol, mic=mic, isin=isin, name=name, currency=currency)

    pe = _to_float(highlights.get("PERatio") or valuation.get("TrailingPE"))
    eps_ttm = _to_float(highlights.get("EarningsShare") or highlights.get("DilutedEpsTTM"))

    div_yield = _to_float(highlights.get("DividendYield"))
    # DividendYield may be percent or decimal depending on provider; you will normalize
    # by checking typical magnitudes in tests.
    # Strategy: if > 1.0 assume percent; else decimal.
    if div_yield is not None and div_yield > 1.0:
        div_yield = div_yield / 100.0

    eps_annual = _extract_eps_annual(fundamentals)

    price = PricePoint(asof=asof, close=float(close), currency=currency or "NOK")
    earnings = EarningsInfo(asof=asof, eps_ttm=eps_ttm, pe_ttm=pe, eps_annual=eps_annual)
    dividends = DividendInfo(asof=asof, ttm_dividend_per_share=None, dividend_yield=div_yield)

    return FundamentalsSnapshot(
        instrument=instrument,
        asof=asof,
        price=price,
        earnings=earnings,
        dividends=dividends,
        sector=sector,
        industry=industry,
        extra=None,  # optionally store raw payload for debugging
    )