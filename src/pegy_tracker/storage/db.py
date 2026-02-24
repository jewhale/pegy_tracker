from __future__ import annotations
import sqlite3
from pathlib import Path

def connect(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con

def init_db(db_path: str, schema_path: str) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with connect(db_path) as con, open(schema_path, "r", encoding="utf-8") as f:
        con.executescript(f.read())