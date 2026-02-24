from __future__ import annotations
from pegy_tracker.markets.base import SimpleMarket


class NorwayOslo(SimpleMarket):
    """
    Norway / Euronext Oslo.
    EODHD commonly uses '.OL' suffix for Oslo-listed instruments.
    """
    mic = "XOSL"
    eodhd_exchange_code = "OL"  # provider-specific convention

    def __init__(self):
        super().__init__(mic=self.mic)

    def normalize_symbol(self, raw: str) -> str:
        # EODHD typically returns already as "EQNR.OL" or "EQNR.OL" / "EQNR"
        # This keeps it consistent.
        raw = raw.strip()
        if raw.endswith(".OL"):
            return raw
        # Some lists use plain tickers; append suffix
        return f"{raw}.OL"

    def default_symbols(self):
        # convenience initial universe
        return ["EQNR.OL", "DNB.OL", "NHY.OL", "TEL.OL", "ORK.OL"]