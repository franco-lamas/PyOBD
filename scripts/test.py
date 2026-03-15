import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..")))

from pyobd import BymaData

client = BymaData()



print("=== Equity Profile (campo/valor format) ===")
equity_prof = client.get_equity_profile("A3")
print(equity_prof)
print()

client.close()