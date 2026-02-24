# pegy-tracker

Track PEG/PEGY-style valuation metrics using pluggable market data providers (starting with Alpha Vantage),
store daily snapshots in SQLite, and screen for potentially undervalued stocks.

This repo is intentionally structured so that:
- **providers/** handles all API calls + mapping into normalized domain models
- **calculations/** contains pure logic (easy to unit test)
- **storage/** persists snapshots
- **screening/** evaluates rules

> Initial focus: Norwegian stocks (Euronext Oslo / MIC: XOSL), but the design supports adding more markets/providers.

---

## Quickstart

### 1) Create a virtual environment and install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -U pip
pip install -e ".[dev]"
```

### 2) Configure environment variables

Copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
```

### 3) Run a smoke test

Once you have the repo structure in place, run:

```bash
pegy --provider alphavantage --market norway --symbols EQNR.OL DNB.OL NHY.OL
```

This will:
- initialize a SQLite db (default: `data/pegy.db`)
- fetch **GLOBAL_QUOTE** + **EARNINGS** for each symbol
- map into normalized models
- compute any enabled metrics (start with EPS CAGR; PEGY later if you add dividends)
- store a snapshot

---

## Environment variables

- `ALPHAVANTAGE_APIKEY` (required): your Alpha Vantage API key
- `PEGY_DB_PATH` (optional): default database path (defaults to `data/pegy.db`)

---

## Repo layout (high-level)

```
src/pegy_tracker/
  providers/        # API clients + mappers
  markets/          # market conventions (symbols, MIC, etc.)
  domain/           # dataclasses and normalized models
  calculations/     # pure metric logic (CAGR, PEGY, validation)
  storage/          # sqlite + repositories
  screening/        # undervalue rules / scoring
  orchestration/    # pipelines (fetch -> compute -> store)
  cli/              # entrypoints
```

---

## Development

### Run tests
```bash
pytest
```

### Format / lint
```bash
ruff check .
ruff format .
mypy
```

---

## Notes about Alpha Vantage + international symbols

Alpha Vantage supports international tickers, but symbol formats can differ by exchange.
For Norway, test what Alpha Vantage expects for Oslo listings (e.g. `EQNR.OL` vs other suffixes).
The `markets/norway.py` normalizer is the right place to enforce a single canonical format.

---

## License

MIT (recommended). Add `LICENSE` if you want.
