from __future__ import annotations
from datetime import date
from typing import Iterable, Optional

from pegy_tracker.providers.base import MarketDataProvider, MarketUniverse
from pegy_tracker.domain.models import InstrumentId, FundamentalsSnapshot
from pegy_tracker.providers.eodhd.client import EodhdClient
from pegy_tracker.providers.eodhd.mapper import map_eodhd_to_snapshot


class EodhdProvider(MarketDataProvider):
    name = "eodhd"

    def __init__(self, client: EodhdClient):
        self.client = client

    def list_equities(self, market: MarketUniverse) -> Iterable[InstrumentId]:
        # For Norway you’ll likely use exchange_code "OL" (EODHD convention).
        # The MarketUniverse can provide that mapping.
        exchange_code = getattr(market, "eodhd_exchange_code", None)
        if not exchange_code:
            raise ValueError(f"Market {market.mic} missing eodhd_exchange_code")

        items = self.client.exchange_list(exchange_code)
        for it in items:
            sym = it.get("Code") or it.get("code") or it.get("Symbol")
            if not sym:
                continue
            symbol = market.normalize_symbol(sym)
            yield InstrumentId(symbol=symbol, mic=market.mic, isin=it.get("ISIN"), name=it.get("Name"))

    def get_fundamentals_snapshot(
        self, instrument: InstrumentId, asof: Optional[date] = None
    ) -> FundamentalsSnapshot:
        fundamentals = self.client.fundamentals(instrument.symbol)
        latest_bar = self.client.eod_latest_close(instrument.symbol)
        return map_eodhd_to_snapshot(
            symbol=instrument.symbol,
            mic=instrument.mic,
            fundamentals=fundamentals,
            latest_bar=latest_bar,
            asof=asof,
        )