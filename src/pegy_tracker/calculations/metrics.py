from __future__ import annotations
from typing import Dict, Optional, List, Tuple

def cagr(start: float, end: float, years: float) -> Optional[float]:
    if years <= 0:
        return None
    if start <= 0 or end <= 0:
        return None
    return (end / start) ** (1.0 / years) - 1.0


def eps_cagr_from_annual(eps_annual: Dict[int, float], years: int = 5) -> Optional[float]:
    """
    Uses the most recent year and the year-years point if available.
    Example: years=5 means need eps at t-5 and t.
    """
    if not eps_annual:
        return None
    ys = sorted(eps_annual.keys())
    y_end = ys[-1]
    y_start = y_end - years
    if y_start not in eps_annual:
        return None

    return cagr(eps_annual[y_start], eps_annual[y_end], years)