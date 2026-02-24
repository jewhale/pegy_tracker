from __future__ import annotations
from pegy_tracker.providers.base import MarketUniverse


class SimpleMarket(MarketUniverse):
    def __init__(self, mic: str):
        self._mic = mic

    @property
    def mic(self) -> str:
        return self._mic