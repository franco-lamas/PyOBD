from pyobd import BymaData

client = BymaData()



print("=== Equity Profile (campo/valor format) ===")
equity_prof = client.get_equity_profile("AL30D")
print(equity_prof)
print()

client.close()