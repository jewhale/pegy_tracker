from __future__ import annotations
import requests
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class EodhdClient:
    token: str
    base_url: str = "https://eodhd.com/api"

    def _get(self, path: str, params: Optional[dict] = None) -> Any:
        params = dict(params or {})
        params["api_token"] = self.token
        params.setdefault("fmt", "json")
        url = f"{self.base_url}/{path.lstrip('/')}"
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def fundamentals(self, symbol: str) -> Dict[str, Any]:
        return self._get(f"fundamentals/{symbol}")

    def eod_latest_close(self, symbol: str) -> Dict[str, Any]:
        # get last available daily bar (limit=1)
        # NOTE: EODHD supports different params; adjust as needed.
        data = self._get(f"eod/{symbol}", params={"period": "d", "limit": 1})
        return data[-1] if isinstance(data, list) and data else {}
    
    def exchange_list(self, exchange_code: str) -> Any:
        # "exchange-symbol-list" is common in EODHD; confirm exact endpoint in your tests.
        return self._get(f"exchange-symbol-list/{exchange_code}")