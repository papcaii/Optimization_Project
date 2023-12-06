from ortools.sat.python import cp_model

import time
from itertools import chain

inp_handle = open("data.inp", "r")

# N, M, K
nStu, nProf, nCouncil = map(int, inp_handle.readline().split())

minStu, maxStu, minProf, maxProf, minMatchThesis, minMachProf = map(int, inp_handle.readline().split())

thesis_data = [[] for i in range(nStu)]

for i in range(nStu):
    data = inp_handle.readline().strip().split(" ")
    thesis_data[i] = list(map(int, data))

prf_data = [[0 for __ in range(nProf)] for _ in range(nStu)]

for i in range(nStu):
    data = inp_handle.readline().strip().split(" ")
    prf_data[i] = list(map(int, data))

data = inp_handle.readline().strip().split(" ")
thesis_guide = list(map(int, data))

print(thesis_data)
print(prf_data)
print(thesis_guide)


def solve(getMax=0):
    model = cp_model.CpModel()

    # Assign student to council
    # set up cs: council + student
    cs = [[0 for _ in range(nStu)] for __ in range(nCouncil)]
    for b in range(nCouncil):
        for i in range(nStu):
            cs[b][i] = model.NewBoolVar(f'cs[{b}, {i}]')

    # Assign professor to council
    # set up cp: council + professor
    cp = [[0 for _ in range(nProf)] for __ in range(nCouncil)]
    for b in range(nCouncil):
        for t in range(nProf):
            cp[b][t] = model.NewBoolVar(f'cp[{b}, {t}]')
