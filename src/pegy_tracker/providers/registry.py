from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Type

from pegy_tracker.providers.base import MarketDataProvider


@dataclass
class ProviderRegistry:
    providers: Dict[str, MarketDataProvider]

    def get(self, name: str) -> MarketDataProvider:
        if name not in self.providers:
            raise KeyError(f"Unknown provider '{name}'. Available: {list(self.providers)}")
        return self.providers[name]