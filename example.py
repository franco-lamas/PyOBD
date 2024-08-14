from PyOBD import openBYMAdata

PyOBD=openBYMAdata()

print(PyOBD.get_bluechips())
print(PyOBD.get_corporateBonds())
print(PyOBD.indices())
print(PyOBD.get_options())
print(PyOBD.marketResume())
print(PyOBD.byma_news())
print(PyOBD.income_statement(ticker="ALUA"))

