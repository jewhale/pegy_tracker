from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable, Optional, List

from pegy_tracker.domain.models import InstrumentId, FundamentalsSnapshot


class MarketUniverse(ABC):
    """Encapsulates symbol formats, MIC, and how to list instruments in a market."""
    @property
    @abstractmethod
    def mic(self) -> str: ...

    @abstractmethod
    def normalize_symbol(self, raw: str) -> str: ...
    
    @abstractmethod
    def default_symbols(self) -> List[str]:
        """Optional convenience starter list."""
        return []


class MarketDataProvider(ABC):
    """Provider interface: fetch raw data and return normalized snapshots."""
    name: str

    @abstractmethod
    def list_equities(self, market: MarketUniverse) -> Iterable[InstrumentId]:
        """Return all equities in the market (or as many as provider supports)."""

    @abstractmethod
    def get_fundamentals_snapshot(
        self,
        instrument: InstrumentId,
        asof: Optional[date] = None
    ) -> FundamentalsSnapshot:
        """Fetch price + fundamentals needed for calculations."""