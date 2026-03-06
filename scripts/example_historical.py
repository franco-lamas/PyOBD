#!/usr/bin/env python3
"""
PyOBD — Example: Historical OHLCV data

Downloads daily historical data for a symbol and prints summary stats.
"""

from pyobd import BymaData

client = BymaData()

symbol = "AL30 24HS"
from_date = "2025-06-01"
to_date = "2025-12-31"

print(f"Downloading historical data for {symbol} ...")
df = client.get_daily_history(symbol, from_date, to_date, resolution="D")

print(f"\n{len(df)} trading days from {from_date} to {to_date}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nLast 5 rows:\n{df.tail()}")
print(f"\nSummary statistics:\n{df.describe()}")

# Optionally save to CSV
# df.to_csv(f"{symbol.replace(' ', '_')}_history.csv", index=False)
# print(f"\nSaved to {symbol.replace(' ', '_')}_history.csv")

client.close()
print("\nDone.")
