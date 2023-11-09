from PyOBD.PyOBD import openBYMAdata

PyOBD=openBYMAdata()

print(PyOBD.get_bluechips())

print(PyOBD.get_futures())