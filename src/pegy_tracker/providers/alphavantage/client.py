from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import requests


class AlphaVantageError(RuntimeError):
    pass


@dataclass
class AlphaVantageClient:
    apikey: str
    base_url: str = "https://www.alphavantage.co/query"

    def _get(self, params: Dict[str, str]) -> Dict[str, Any]:
        params = dict(params)
        params["apikey"] = self.apikey

        r = requests.get(self.base_url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()

        # Alpha Vantage error/limit payloads often contain these keys:
        if isinstance(data, dict):
            if "Error Message" in data:
                raise AlphaVantageError(data["Error Message"])
            if "Information" in data:
                # usually rate limit / throttling info
                raise AlphaVantageError(data["Information"])
            if "Note" in data:
                raise AlphaVantageError(data["Note"])

        return data

    def global_quote(self, symbol: str) -> Dict[str, Any]:
        return self._get({"function": "GLOBAL_QUOTE", "symbol": symbol})

    def earnings(self, symbol: str) -> Dict[str, Any]:
        return self._get({"function": "EARNINGS", "symbol": symbol})