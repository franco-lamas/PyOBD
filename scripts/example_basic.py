#!/usr/bin/env python3
"""
PyOBD — Example: Basic usage

Demonstrates importing the library and calling its main methods.
No authentication required.
"""

from pyobd import BymaData

client = BymaData()

# ── 1. Market status ──────────────────────────────────────────────────
print("=" * 60)
print("  Market Time")
print("=" * 60)
mt = client.get_market_time()
print(f"  Opening : {mt['marketOpeningTime']}")
print(f"  Closing : {mt['marketClosingTime']}")
print(f"  Work day: {mt['isWorkingDay']}")
print(f"  Timezone: {mt['timezone']}")

# ── 2. Indices ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  Equity Indices")
print("=" * 60)
indices = client.get_indices()
cols = [c for c in ["symbol", "trade", "variation"] if c in indices.columns]
print(indices[cols].to_string(index=False))

# ── 3. Blue chips ────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  Blue chips (Top 5)")
print("=" * 60)
equity = client.get_bluechips()  # formerly get_leading_equity
if len(equity) > 0:
    show = [c for c in ["symbol", "trade", "volume", "variation"] if c in equity.columns]
    print(equity[show].head().to_string(index=False))
else:
    print("  (no data — market may be closed)")

# ── 4. CEDEARs ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  CEDEARs (Top 5)")
print("=" * 60)
cedears = client.get_cedears()
if len(cedears) > 0:
    show = [c for c in ["symbol", "trade", "volume"] if c in cedears.columns]
    print(cedears[show].head().to_string(index=False))
else:
    print("  (no data — market may be closed)")

client.close()
print("\nDone.")
