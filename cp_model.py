# ================================   IDEA    ================================== #
# Just a CP Model from Ortools
# Loop all solutions then choose the optimal
# ============================================================================= #

from ortools.sat.python import cp_model

# N, M, K
num_thesis, num_prof, num_council = map(int, input().split())
min_thesis, max_thesis, min_prof, max_prof, min_MatchThesis, min_MatchProf = map(int, input().split())

thesis_data = []
for _ in range(num_thesis):
    thesis_data.append([int(x) for x in input().strip().split(" ")])

prf_data = []
for _ in range(num_thesis):
    prf_data.append([int(x) for x in input().strip().split(" ")])

thesis_advisor = [int(x) for x in input().strip().split(" ")]


def solve(get_max=0):
    model = cp_model.CpModel()

    # Assign thesis to council
    # set up cs: council + thesis
    ct = [[0 for _ in range(num_thesis)] for __ in range(num_council)]
    for council in range(num_council):
        for k in range(num_thesis):
            ct[council][k] = model.NewBoolVar(f'ct[{council}, {k}]')

    # Assign professor to council
    # set up cp: council + professor
    cp = [[0 for _ in range(num_prof)] for __ in range(num_council)]
    for council in range(num_council):
        for i in range(num_prof):
            cp[council][i] = model.NewBoolVar(f'cp[{council}, {i}]')

    # Each thesis k is assigned to a council and only one
    for k in range(num_thesis):
        model.AddExactlyOne(ct[council][k] for council in range(num_council))

    # Each professor i is assigned to a council and only one
    for i in range(num_prof):
        model.AddExactlyOne(cp[council][i] for council in range(num_council))

    for council in range(num_council):
        # Number of thesis in a council >= min_thesis and <= max_thesis
        model.Add(sum(ct[council][k] for k in range(num_thesis)) >= min_thesis)
        model.Add(sum(ct[council][k] for k in range(num_thesis)) <= max_thesis)

        # Number of professor in a council >= min_prof and <= max_prof:
        model.Add(sum(ct[council][i] for i in range(num_prof)) >= min_prof)
        model.Add(sum(ct[council][i] for i in range(num_prof)) <= max_prof)

    # The similarity between two thesis within same council >= min_MatchThesis
    for council in range(num_council):
        for i in range(num_thesis):
            for j in range(i + 1, num_thesis):
                if thesis_data[i][j] < min_MatchThesis:
                    model.AddAtMostOne([ct[council][i], ct[council][j]])

    # The similarity between each thesis and professor within same council >= min_MatchProf
    # Thesis cannot be in the same council with its advisor
    for council in range(num_council):
        for k in range(num_thesis):
            for i in range(num_prof):
                if prf_data[k][i] < min_MatchProf or (i + 1) == thesis_advisor[k]:
                    model.AddAtMostOne(ct[council][k], cp[council][i])

    # IF we want to get the maximum similarity, BUT this will significantly increase time
    if get_max == 1:
        objective_terms = []

        # Thesis-Thesis similarity
        for council in range(num_council):
            for i in range(num_thesis):
                for j in range(i + 1, num_thesis):
                    tt = model.NewBoolVar(f'tt[{i}, {j}]')
                    model.AddBoolAnd([ct[council][i], ct[council][j]]).OnlyEnforceIf(tt)
                    similarity = thesis_data[i][j] * tt
                    objective_terms.append(similarity)

        # Thesis-Professor similarity
        for council in range(num_council):
            for k in range(num_thesis):
                for i in range(num_prof):
                    tp = model.NewBoolVar(f'tp[{k}, {i}]')
                    model.AddBoolAnd([ct[council][k], cp[council][i]]).OnlyEnforceIf(tp)
                    similarity = prf_data[k][i] * tp
                    objective_terms.append(similarity)

        model.Maximize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    solver.parameters.enumerate_all_solutions = False
    status = solver.Solve(model)

    # Print solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(num_thesis)
        for k in range(num_thesis):
            for council in range(num_council):
                if solver.BooleanValue(ct[council][k]):
                    print(f"{council + 1}", end=' ')

        print()
        print(num_prof)

        for i in range(num_prof):
            for council in range(num_council):
                if solver.BooleanValue(cp[council][i]):
                    print(f"{council + 1}", end=' ')

    else:
        print("No solution found.")


solve()
