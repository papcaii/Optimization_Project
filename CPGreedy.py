# ================================   IDEA    ================================== #
# Total compatibility = Thesis-Thesis compatibility + Thesis_Professor
# So I will assign thesis first with cp_model ---> Loop all feasible assignments
# Then handle each feasible thesis assignment with SolutionHandle class
# Then I will search for best professor assignment with LocalGreedy class
# ============================================================================= #

import random
import numpy as np
from ortools.sat.python import cp_model
import time

# Read input from the file
# N, M, K
num_thesis, num_prof, num_council = map(int, input().split())
min_thesis, max_thesis, min_prof, max_prof, min_MatchThesis, min_MatchProf = map(int, input().split())

# Read thesis_data as a NumPy array
thesis_data = np.zeros((num_thesis, num_thesis), dtype=int)
for i in range(num_thesis):
    thesis_data[i] = np.array([int(x) for x in input().strip().split(" ")])

# Read prf_data as a NumPy array
prf_data = np.zeros((num_thesis, num_prof), dtype=int)
for i in range(num_thesis):
    prf_data[i] = np.array([int(x) for x in input().strip().split(" ")])

# Read thesis_advisor as a NumPy array
thesis_advisor = np.array([int(x) for x in input().strip().split(" ")])
council_array = list(range(num_council))


def calc_tt_compatibility(thesis_array):
    compatibility = 0
    for i in range(num_thesis):
        for j in range(i + 1, num_thesis):
            if thesis_array[i] == thesis_array[j]:
                compatibility += thesis_data[i][j]
    return compatibility


class LocalGreedy:
    """Local search + Greedy method for professor assignment"""

    def __init__(self, thesis_array):
        self.thesis_array = thesis_array
        # self.cp[i][j] = a ---> If a=1 it means professor <j> is assigned to council <i>, else a=0
        self.cp = [[0 for _ in range(num_prof)] for _ in range(num_council)]
        self.tp_compatibility = 0
        self.councils = [0] * num_council
        self.priority_councils = list(range(num_council))

        # councils[i] = a ---> it means council <i> is having the list <a> of theses assigned to it
        for i in range(num_thesis):
            council = thesis_array[i] - 1
            if self.councils[council] == 0:
                self.councils[council] = [i]
            else:
                self.councils[council].append(i)

    # Check if the assignment is conflicted with our constraints
    # And return the compatibility of this assignment
    def check_violation(self, professor, council):

        # Number of professors in each council <= max_prof
        if sum(self.cp[council]) >= max_prof:
            return False

        cur_compatibility = 0
        for thesis in self.councils[council]:
            # Professor can not be in the same council with the thesis they guide
            if (professor + 1) == thesis_advisor[thesis]:
                return False
            cur_compatibility += prf_data[thesis][professor]

        return cur_compatibility

    def prof_to_council(self, professor):
        max_list = []
        max_compatibility = 0

        # The number of professors in each council >= min_prof
        # So I will prioritize the councils not having enough professor yet
        if self.priority_councils:
            for cur_council in self.priority_councils:
                cur_compatibility = self.check_violation(professor, cur_council)
                if cur_compatibility < max_compatibility:
                    continue

                elif cur_compatibility > max_compatibility:
                    max_list = []
                    max_compatibility = cur_compatibility

                max_list.append(cur_council)

            if max_compatibility != 0:
                chosen_council = random.choice(max_list)
                # Note in cp that is chosen
                self.cp[chosen_council][professor] = 1
                self.tp_compatibility += max_compatibility
                # Remove that councils from priority list if it has enough professors
                if sum(self.cp[chosen_council]) >= min_prof:
                    self.priority_councils.remove(chosen_council)
                return True

        # If no priority, then normally assign professor to councils:
        for cur_council in council_array:
            cur_compatibility = self.check_violation(professor, cur_council)
            if cur_compatibility < max_compatibility:
                continue

            elif cur_compatibility > max_compatibility:
                max_list = []
                max_compatibility = cur_compatibility

            max_list.append(cur_council)

        if max_compatibility != 0:
            chosen_council = random.choice(max_list)
            # Note in cp that is chosen
            self.cp[chosen_council][professor] = 1
            self.tp_compatibility += max_compatibility
            return True

        # If no council valid, then loop to another thesis assignment
        return False

    def solver(self):
        for i in range(num_prof):
            success = self.prof_to_council(i)
            if not success:
                return False

        # Successfully assign all professor
        professor_array = []

        for professor in range(num_prof):
            for council in range(num_council):
                if self.cp[council][professor]:
                    professor_array.append(council + 1)
                    break

        objective_value = calc_tt_compatibility(self.thesis_array) + self.tp_compatibility

        return [professor_array, objective_value]


class SolutionHandle(cp_model.CpSolverSolutionCallback):
    """Handle intermediate solutions."""

    def __init__(self, ct):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.ct = ct
        self.solutions = []
        self.solution_count = 0
        self.optimal_value = 0

    def on_solution_callback(self):
        thesis_array = []

        # thesis_array[i]=a ---> The thesis <i> is assigned to council <a>
        for thesis in range(num_thesis):
            for council in range(num_council):
                if self.Value(self.ct[council, thesis]):
                    thesis_array.append(council + 1)
                    break

        # Local search for each thesis assignments
        my_greedy = LocalGreedy(thesis_array)
        answer = my_greedy.solver()

        # If LocalGreedy give out solution
        if answer:
            self.solution_count += 1
            prof_array, objective_value = answer
            if objective_value > self.optimal_value:
                self.optimal_value = objective_value
                self.solutions = [thesis_array, prof_array]


# If you want to print out solution count, runtime,... (you can config this) set log to True
def solve(log=False):
    start_time = time.time()
    model = cp_model.CpModel()

    # Assign thesis to council
    # set up ct: council + thesis
    ct = {}
    for council in range(num_council):
        for thesis in range(num_thesis):
            ct[council, thesis] = model.NewBoolVar(f'ct[{council}, {thesis}]')

    # Each thesis k is assigned to a council and only one
    for thesis in range(num_thesis):
        model.AddExactlyOne(ct[council, thesis] for council in range(num_council))

    for council in range(num_council):
        # Number of thesis in a council >= min_thesis and <= max_thesis
        model.Add(sum(ct[council, thesis] for thesis in range(num_thesis)) >= min_thesis)
        model.Add(sum(ct[council, thesis] for thesis in range(num_thesis)) <= max_thesis)

    # Generate all feasible thesis assignments, then handle it with SolutionHandle
    solver = cp_model.CpSolver()
    # Set time limit for the solver
    solver.parameters.max_time_in_seconds = 10.0
    solution_handle = SolutionHandle(ct)
    # solution_handle will be called for every solution
    solver.SearchForAllSolutions(model, solution_handle)

    end_time = time.time()

    # Print our answer
    print(num_thesis)
    for _ in solution_handle.solutions[0]:
        print(_, end=' ')
    print()
    print(num_prof)
    for _ in solution_handle.solutions[1]:
        print(_, end=' ')
    if log:
        print(f'\n\nObjective value: {solution_handle.optimal_value}')
        print(f'Running time: {end_time - start_time}')
        print(f'Total solutions: {solution_handle.solution_count}')


solve(log=True)
