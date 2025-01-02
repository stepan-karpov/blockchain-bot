CREATE TABLE IF NOT EXISTS testing.currencies_history (
  currency TEXT NOT NULL,
  open_time BIGINT,
  value NUMERIC(30, 15),
  high NUMERIC(30, 15),
  low NUMERIC(30, 15),
  close NUMERIC(30, 15),
  volume NUMERIC(30, 15),
  close_time BIGINT,
  quote_asset_volume NUMERIC(30, 15),

  PRIMARY KEY (currency, open_time, close_time)
);

CREATE TABLE IF NOT EXISTS testing.currencies_values(
  currency TEXT NOT NULL,
  timestamp BIGINT,
  value NUMERIC(30, 15),

  PRIMARY KEY (currency, timestamp)
);