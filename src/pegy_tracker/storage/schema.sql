CREATE TABLE IF NOT EXISTS instruments (
  symbol TEXT PRIMARY KEY,
  mic TEXT NOT NULL,
  isin TEXT,
  name TEXT,
  currency TEXT
);

CREATE TABLE IF NOT EXISTS snapshots (
  asof TEXT NOT NULL,
  symbol TEXT NOT NULL,
  mic TEXT NOT NULL,
  price REAL,
  currency TEXT,
  pe REAL,
  eps_ttm REAL,
  div_yield REAL,
  eps_cagr_5y REAL,
  pegy REAL,
  sector TEXT,
  industry TEXT,
  flags TEXT,
  PRIMARY KEY (asof, symbol),
  FOREIGN KEY (symbol) REFERENCES instruments(symbol)
);