from __future__ import annotations
from typing import List, Optional


def validate_positive(x: Optional[float], field: str, flags: List[str]) -> bool:
    if x is None:
        flags.append(f"missing:{field}")
        return False
    if x <= 0:
        flags.append(f"nonpositive:{field}")
        return False
    return True


def cap_outliers(x: float, low: float, high: float, field: str, flags: List[str]) -> float:
    if x < low:
        flags.append(f"clipped_low:{field}")
        return low
    if x > high:
        flags.append(f"clipped_high:{field}")
        return high
    return x