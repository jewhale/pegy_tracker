from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    eodhd_token: str

    @staticmethod
    def from_env() -> "Settings":
        token = os.environ.get("EODHD_TOKEN")
        if not token:
            raise RuntimeError("EODHD_TOKEN not set")
        return Settings(eodhd_token=token)