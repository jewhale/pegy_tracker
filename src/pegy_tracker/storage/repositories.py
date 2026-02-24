from __future__ import annotations
import sqlite3
from typing import Optional

from pegy_tracker.domain.models import InstrumentId, FundamentalsSnapshot, MetricResult


class InstrumentRepository:
    def __init__(self, con: sqlite3.Connection):
        self.con = con

    def upsert(self, inst: InstrumentId) -> None:
        self.con.execute(
            """
            INSERT OR REPLACE INTO instruments(symbol, mic, isin, name, currency)
            VALUES (?, ?, ?, ?, ?)
            """,
            (inst.symbol, inst.mic, inst.isin, inst.name, inst.currency),
        )


class SnapshotRepository:
    def __init__(self, con: sqlite3.Connection):
        self.con = con

    def insert_snapshot(self, snap: FundamentalsSnapshot, result: Optional[MetricResult]) -> None:
        metrics = result.metrics if result else {}
        flags = ",".join(result.flags) if result else ""

        self.con.execute(
            """
            INSERT OR REPLACE INTO snapshots(
              asof, symbol, mic, price, currency, pe, eps_ttm, div_yield, eps_cagr_5y, pegy,
              sector, industry, flags
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(snap.asof),
                snap.instrument.symbol,
                snap.instrument.mic,
                snap.price.close,
                snap.price.currency,
                metrics.get("pe"),
                snap.earnings.eps_ttm,
                metrics.get("div_yield"),
                metrics.get("eps_cagr_5y") or metrics.get("eps_cagr_5y"),  # adjust if you use 3y/5y
                metrics.get("pegy"),
                snap.sector,
                snap.industry,
                flags,
            ),
        )