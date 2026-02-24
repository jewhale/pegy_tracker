from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class UndervalueRule:
    max_pegy: float = 1.0
    min_growth: float = 0.05
    min_div_yield: float = 0.01

    def is_undervalued(self, pegy: Optional[float], growth: Optional[float], div_yield: Optional[float]) -> bool:
        if pegy is None or growth is None or div_yield is None:
            return False
        return (pegy <= self.max_pegy) and (growth >= self.min_growth) and (div_yield >= self.min_div_yield)