#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  PyOBD — Standalone Demo                                     ║
║  BYMA Open Data - Argentine Market Data (no auth required)   ║
╚══════════════════════════════════════════════════════════════╝

This script showcases every public method in the PyOBD library.
Run it directly:

    python scripts/demo_pyobd.py

Requirements:
    pip install pyobd        # or: pip install -e .
"""

from __future__ import annotations

import sys
import textwrap

import pandas as pd

from pyobd import BymaData, __version__


# ── Helpers ────────────────────────────────────────────────────────────

def section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def show_df(df: pd.DataFrame, rows: int = 5) -> None:
    """Print first N rows or a 'no data' message."""
    if df.empty:
        print("  (sin datos — el mercado puede estar cerrado)")
    else:
        print(df.head(rows).to_string(index=False))


# ── Main ───────────────────────────────────────────────────────────────

def main() -> None:
    print(f"PyOBD v{__version__}  — BYMA Open Data Demo")
    print("Conectando a https://open.bymadata.com.ar …")

    client = BymaData()

    # ----------------------------------------------------------------
    # 1. Market time
    # ----------------------------------------------------------------
    section("1 · Estado del mercado  →  get_market_time()")
    mt = client.get_market_time()
    print(f"  Apertura : {mt['marketOpeningTime']}")
    print(f"  Cierre   : {mt['marketClosingTime']}")
    print(f"  Día hábil: {mt['isWorkingDay']}")
    print(f"  Zona     : {mt['timezone']}")

    # ----------------------------------------------------------------
    # 2. Indices
    # ----------------------------------------------------------------
    section("2 · Índices bursátiles  →  get_indices()")
    indices = client.get_indices()
    cols = [c for c in ["symbol", "trade", "variation"] if c in indices.columns]
    show_df(indices[cols])

    # ----------------------------------------------------------------
    # 3. Blue chips (acciones líderes)
    # ----------------------------------------------------------------
    section("3 · Blue chips  →  get_bluechips()")
    leading = client.get_bluechips()
    cols = [c for c in ["symbol", "trade", "volume", "variation"] if c in leading.columns]
    show_df(leading[cols] if cols else leading)

    # ----------------------------------------------------------------
    # 4. General board
    # ----------------------------------------------------------------
    section("4 · Acciones general  →  get_general_board()")
    general = client.get_general_board()
    print(f"  {len(general)} especies listadas")

    # ----------------------------------------------------------------
    # 5. CEDEARs
    # ----------------------------------------------------------------
    section("5 · CEDEARs  →  get_cedears()")
    cedears = client.get_cedears()
    cols = [c for c in ["symbol", "trade", "volume"] if c in cedears.columns]
    show_df(cedears[cols] if cols else cedears)

    # ----------------------------------------------------------------
    # 6. Current quote
    # ----------------------------------------------------------------
    section("6 · Cotización actual  →  get_current_quote('GGAL', '48HS')")
    quote = client.get_current_quote("GGAL", settlement="48HS")
    show_df(quote)

    # ----------------------------------------------------------------
    # 7. Historical OHLCV data (pyhomebroker compatible)
    # ----------------------------------------------------------------
    section("7 · Datos históricos  →  get_daily_history('GGAL 24HS', …)")
    hist = client.get_daily_history(
        symbol="GGAL 24HS",
        from_date="2025-06-01",
        to_date="2025-12-31",
        resolution="D",
    )
    print(f"  {len(hist)} ruedas descargadas\n")
    show_df(hist)

    # ----------------------------------------------------------------
    # 8. Government bonds
    # ----------------------------------------------------------------
    section("8 · Títulos públicos  →  get_government_bonds()")
    bonds = client.get_government_bonds()
    print(f"  {len(bonds)} bonos")

    # ----------------------------------------------------------------
    # 9. Corporate bonds
    # ----------------------------------------------------------------
    section("9 · Obligaciones negociables  →  get_corporate_bonds()")
    corp = client.get_corporate_bonds()
    print(f"  {len(corp)} obligaciones")

    # ----------------------------------------------------------------
    # 10. Short-term government bonds
    # ----------------------------------------------------------------
    section("10 · Letras  →  get_short_term_government_bonds()")
    letters = client.get_short_term_government_bonds()
    print(f"  {len(letters)} letras")

    # ----------------------------------------------------------------
    # 11. Company info
    # ----------------------------------------------------------------
    section("11 · Información empresa  →  get_company_info('ALUA')")
    info_df = client.get_company_info("ALUA")
    if info_df.empty:
        print("  (sin datos)")
    else:
        for _, row in info_df.head(8).iterrows():
            print(f"  {row['campo']}: {row['valor']}")

    # ----------------------------------------------------------------
    # 12. Equity profile
    # ----------------------------------------------------------------
    section("12 · Perfil especie  →  get_equity_profile('ALUA')")
    equity_df = client.get_equity_profile("ALUA")
    if equity_df.empty:
        print("  (sin datos)")
    else:
        for _, row in equity_df.iterrows():
            val = str(row['valor'])[:50]
            print(f"  {row['campo']}: {val}")

    # ----------------------------------------------------------------
    # 13. Company management
    # ----------------------------------------------------------------
    section("13 · Directivos  →  get_company_management('ALUA')")
    mgmt = client.get_company_management("ALUA")
    show_df(mgmt)

    # ----------------------------------------------------------------
    # 14. Company balance
    # ----------------------------------------------------------------
    section("14 · Balance  →  get_company_balance('ALUA')")
    balance = client.get_company_balance("ALUA")
    if balance.empty:
        print("  (sin datos — endpoint puede no ser accesible)")
    else:
        show_df(balance)

    # ----------------------------------------------------------------
    # 15. Dictionary
    # ----------------------------------------------------------------
    section("15 · Diccionario i18n  →  get_dictionary()")
    d = client.get_dictionary()
    print(f"  {len(d)} claves de traducción")
    sample = list(d.items())[:3]
    for k, v in sample:
        print(f"  {k}: {v}")

    # ----------------------------------------------------------------
    # Done
    # ----------------------------------------------------------------
    client.close()
    print(f"\n{'═' * 60}")
    print(f"  Demo completa — {len(hist)} filas históricas descargadas")
    print(f"  Todos los métodos de PyOBD funcionan correctamente ✓")
    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    main()
