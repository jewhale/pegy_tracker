from __future__ import annotations
import os
import argparse

from pegy_tracker.config.settings import Settings
from pegy_tracker.storage.db import connect, init_db
from pegy_tracker.providers.eodhd.client import EodhdClient
from pegy_tracker.providers.eodhd.provider import EodhdProvider
from pegy_tracker.markets.norway import NorwayOslo
from pegy_tracker.calculations.pegy import PegyCalculator
from pegy_tracker.orchestration.pipeline import DailySnapshotPipeline


def build_parser():
    p = argparse.ArgumentParser("pegy-tracker")
    p.add_argument("--db", default="data/pegy.db")
    p.add_argument("--provider", default="eodhd")
    p.add_argument("--market", default="norway")
    p.add_argument("--symbols", nargs="*", default=None)
    return p


def main():
    args = build_parser().parse_args()

    settings = Settings.from_env()

    init_db(args.db, "src/pegy_tracker/storage/schema.sql")
    con = connect(args.db)

    market = NorwayOslo()

    client = EodhdClient(token=settings.eodhd_token)
    provider = EodhdProvider(client=client)

    calculator = PegyCalculator(eps_cagr_years=5)

    pipeline = DailySnapshotPipeline(
        provider=provider,
        market=market,
        calculator=calculator,
        con=con,
    )

    pipeline.run(symbols=args.symbols)
    print("Done.")


if __name__ == "__main__":
    main()