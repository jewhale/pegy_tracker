import sqlite3
from datetime import date

from pegy_tracker.calculations.pegy import PegyCalculator
from pegy_tracker.domain.models import (
    DividendInfo,
    EarningsInfo,
    FundamentalsSnapshot,
    InstrumentId,
    PricePoint,
)
from pegy_tracker.markets.base import SimpleMarket
from pegy_tracker.orchestration.pipeline import DailySnapshotPipeline
from pegy_tracker.providers.base import MarketDataProvider, MarketUniverse


class StubMarket(SimpleMarket):
    def __init__(self) -> None:
        super().__init__(mic="XOSL")

    def normalize_symbol(self, raw: str) -> str:
        return raw

    def default_symbols(self) -> list[str]:
        return ["EQNR.OL"]


class StubProvider(MarketDataProvider):
    name = "stub"

    def list_equities(self, market: MarketUniverse):
        return []

    def get_fundamentals_snapshot(self, instrument: InstrumentId, asof: date | None = None) -> FundamentalsSnapshot:
        snapshot_date = asof or date.today()
        return FundamentalsSnapshot(
            instrument=instrument,
            asof=snapshot_date,
            price=PricePoint(asof=snapshot_date, close=100.0, currency="NOK"),
            earnings=EarningsInfo(asof=snapshot_date, eps_ttm=5.0, pe_ttm=10.0, eps_annual={2019: 1.0, 2024: 2.0}),
            dividends=DividendInfo(asof=snapshot_date, ttm_dividend_per_share=2.0, dividend_yield=0.05),
        )


def test_pipeline_persists_instrument_and_snapshot() -> None:
    con = sqlite3.connect(":memory:")
    with open("src/pegy_tracker/storage/schema.sql", encoding="utf-8") as f:
        con.executescript(f.read())

    pipeline = DailySnapshotPipeline(
        provider=StubProvider(),
        market=StubMarket(),
        calculator=PegyCalculator(),
        con=con,
    )

    pipeline.run(symbols=["EQNR.OL"], asof=date(2024, 1, 1))

    snapshot_count = con.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
    assert snapshot_count == 1
