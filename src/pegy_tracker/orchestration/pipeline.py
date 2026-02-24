from __future__ import annotations
from datetime import date
import sqlite3
from typing import Iterable, Optional

from pegy_tracker.providers.base import MarketDataProvider, MarketUniverse
from pegy_tracker.calculations.pegy import PegyCalculator
from pegy_tracker.storage.repositories import InstrumentRepository, SnapshotRepository
from pegy_tracker.domain.models import InstrumentId


class DailySnapshotPipeline:
    def __init__(
        self,
        provider: MarketDataProvider,
        market: MarketUniverse,
        calculator: PegyCalculator,
        con: sqlite3.Connection,
    ):
        self.provider = provider
        self.market = market
        self.calculator = calculator
        self.inst_repo = InstrumentRepository(con)
        self.snap_repo = SnapshotRepository(con)
        self.con = con

    def run(
        self,
        symbols: Optional[Iterable[str]] = None,
        asof: Optional[date] = None,
    ) -> None:
        asof = asof or date.today()

        if symbols is None:
            symbols = self.market.default_symbols()

        for raw in symbols:
            symbol = self.market.normalize_symbol(raw)
            inst = InstrumentId(symbol=symbol, mic=self.market.mic)

            try:
                snap = self.provider.get_fundamentals_snapshot(inst, asof=asof)
                self.inst_repo.upsert(snap.instrument)
                res = self.calculator.compute(snap)
                self.snap_repo.insert_snapshot(snap, res)
                self.con.commit()
            except Exception as e:
                # log in real code
                self.con.rollback()
                print(f"[WARN] {symbol}: {e}")