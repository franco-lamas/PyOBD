#!/usr/bin/env python3
"""
PyOBD — Example: Company Information

Demonstrates how to retrieve detailed information about companies listed
on BYMA including company info, equity profile, management, and financial data.
"""

from pyobd import BymaData

# Example symbols to query
COMPANIES = ["ALUA", "GGAL", "CEPU"]

client = BymaData()

for symbol in COMPANIES:
    print(f"\n{'=' * 70}")
    print(f"  Company: {symbol}")
    print(f"{'=' * 70}")

    # ── 1. Company Info (sociedad) ──────────────────────────────────
    print(f"\n1. Company Info  →  get_company_info('{symbol}')")
    print(f"{'-' * 70}")

    company_df = client.get_company_info(symbol)

    if company_df.empty:
        print("  (no data available)")
    else:
        # Filter for useful fields and display
        useful_fields = [
            "emisor", "sector", "pais", "ciudad", "calle",
            "telefono", "website", "email", "cierreEjercicio", "actividad"
        ]
        filtered = company_df[company_df["campo"].isin(useful_fields)]

        for _, row in filtered.iterrows():
            campo = row["campo"]
            valor = str(row["valor"]) if row["valor"] else ""
            # Limit long values to 60 chars
            if len(valor) > 60:
                valor = valor[:57] + "..."
            if valor:  # Only show non-empty values
                print(f"  {campo:20s}: {valor}")

    # ── 2. Equity Profile (especie) ─────────────────────────────────
    print(f"\n2. Equity Profile  →  get_equity_profile('{symbol}')")
    print(f"{'-' * 70}")

    equity_df = client.get_equity_profile(symbol)

    if equity_df.empty:
        print("  (no data available)")
    else:
        for _, row in equity_df.iterrows():
            campo = row["campo"]
            valor = str(row["valor"]) if row["valor"] else ""
            print(f"  {campo:20s}: {valor}")

    # ── 3. Company Management ───────────────────────────────────────
    print(f"\n3. Management  →  get_company_management('{symbol}')")
    print(f"{'-' * 70}")

    mgmt = client.get_company_management(symbol)

    if mgmt.empty:
        print("  (no data available)")
    else:
        # Show directors/management in a clean format
        if "cargo" in mgmt.columns and "persona" in mgmt.columns:
            print(f"\n  {'Role':<35} {'Name':<35}")
            print(f"  {'-'*35} {'-'*35}")
            for _, row in mgmt.iterrows():
                cargo = str(row.get("cargo", ""))
                persona = str(row.get("persona", ""))
                # Truncate if needed
                cargo = cargo[:35] if len(cargo) > 35 else cargo
                persona = persona[:35] if len(persona) > 35 else persona
                print(f"  {cargo:<35} {persona:<35}")
        else:
            print(mgmt.to_string(index=False))

    # ── 4. Company Balance ──────────────────────────────────────────
    print(f"\n4. Balance  →  get_company_balance('{symbol}')")
    print(f"{'-' * 70}")

    balance = client.get_company_balance(symbol)

    if balance.empty:
        print("  (no balance sheet data available - endpoint may not be reachable)")
    else:
        print(f"  {len(balance)} line items\n")
        # Show first and last rows
        print("  First 5 items:")
        print(balance.head().to_string(index=False))
        if len(balance) > 5:
            print(f"\n  ... ({len(balance) - 10} more items) ...\n")
            print("  Last 5 items:")
            print(balance.tail().to_string(index=False))

client.close()
print(f"\n{'=' * 70}")
print("  Done.")
print(f"{'=' * 70}\n")
