# PYTHON
import time
import numpy as np
import random

###########
TIME_LIMIT = 10
##########

# =========================== Read input from the file =========================== #
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

priority_councils = set(range(1, num_council))

high_tt = {key: set() for key in range(num_thesis)}

for i in range(num_thesis):
    for j in range(num_thesis):
        cur = thesis_data[i][j]
        if thesis_advisor[i] == thesis_advisor[j]:
            cur = cur * 2
        if cur > 5:
            high_tt[i].add(j)


# ================================================================================ #


class ProfessorGreedy:
    """Greedy method for professor assignment"""

    def __init__(self, thesis_array):
        self.thesis_array = thesis_array
        self.cp = {(council, prof): 0 for council in range(num_council) for prof in range(num_prof)}
        self.tp_compatibility = 0
        self.council_thesis = {key: set() for key in range(num_council)}
        self.priority_councils = list(range(num_council))

        # council_thesis[i] = a ---> it means council <i> is having the list <a> of theses assigned to it
        for i in range(num_thesis):
            self.council_thesis[thesis_array[i] - 1].add(i)

    def calc_tt_compatibility(self):
        compatibility = 0
        for i in range(num_thesis):
            for j in range(i + 1, num_thesis):
                if self.thesis_array[i] == self.thesis_array[j]:
                    compatibility += thesis_data[i][j]
        return compatibility

    # Check if the assignment is conflicted with our constraints
    # And return the compatibility of this assignment
    def check_violation(self, professor, council):

        # Number of professors in each council <= max_prof
        if sum(self.cp[council, prof] for prof in range(num_prof)) >= max_prof:
            return False

        cur_compatibility = 0
        for thesis in self.council_thesis[council]:
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
                self.cp[chosen_council, professor] = 1
                self.tp_compatibility += max_compatibility
                # Remove that councils from priority list if it has enough professors
                if sum(self.cp[chosen_council, _] for _ in range(num_prof)) >= min_prof:
                    self.priority_councils.remove(chosen_council)
                return True

        # If no priority, then normally assign professor to councils:
        for cur_council in range(num_council):
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
            self.cp[chosen_council, professor] = 1
            self.tp_compatibility += max_compatibility
            return True

        # If no council valid, then loop to another thesis assignment
        return False

    def solver(self):
        for prof in range(num_prof):
            success = self.prof_to_council(prof)
            if not success:
                return False

        # Successfully assign all professor
        professor_array = []

        for professor in range(num_prof):
            for council in range(num_council):
                if self.cp[council, professor]:
                    professor_array.append(council + 1)
                    break

        objective_value = self.calc_tt_compatibility() + self.tp_compatibility
        # print(f'Professor: {self.tp_compatibility}')
        # print(f'Thesis: {objective_value - self.tp_compatibility}')

        return [professor_array, objective_value]


class ThesisGreedy:
    """Greedy method for thesis assignment"""

    def __init__(self):
        self.thesis_array = {key: -1 for key in range(num_thesis)}
        self.council_array = {key: set() for key in range(num_council)}

    def add_high_tt(self, target, chosen_council):
        target = list(target)
        remaining_slot = max_thesis - len(self.council_array[chosen_council])

        # while this council is not full
        # I want put as much thesis as possible
        while (remaining_slot > 0) and (len(target) > 0):
            # Randomly get thesis on list
            chosen_thesis = random.choice(target)

            # Check if this thesis is assigned
            if self.thesis_array[chosen_thesis] != -1:
                target.remove(chosen_thesis)
                continue

            self.thesis_array[chosen_thesis] = chosen_council
            self.council_array[chosen_council].add(chosen_thesis)
            target.remove(chosen_thesis)
            remaining_slot -= 1

    def thesis_to_council(self, chosen_thesis):
        chosen_council = -1
        # Prioritize empty council
        for council in range(num_council):
            if len(self.council_array[council]) == 0:
                chosen_council = council
        # No empty council
        if chosen_council == -1:
            potential_council = {key: 0 for key in range(num_council)}
            for council in range(num_council):
                if len(self.council_array[council]) >= max_thesis:  # This council is full
                    potential_council[council] -= 99
                    continue
                cur = 0
                for _ in self.council_array[council]:
                    # We want to put high thesis-thesis pairs together
                    tmp = thesis_data[chosen_thesis][_]
                    if thesis_advisor[_] == thesis_advisor[chosen_thesis]:
                        tmp = tmp * 2
                    cur += tmp
                potential_council[council] = cur
            chosen_council = max(potential_council, key=lambda x: potential_council[x])
        self.thesis_array[chosen_thesis] = chosen_council
        self.council_array[chosen_council].add(chosen_thesis)
        self.add_high_tt(high_tt[chosen_thesis], chosen_council)

    def solver(self):
        for chosen_thesis in sorted(high_tt, key=lambda x: high_tt[x], reverse=True):
            if self.thesis_array[chosen_thesis] != -1:
                continue
            self.thesis_to_council(chosen_thesis)

        return {x: (self.thesis_array[x] + 1) for x in self.thesis_array}


def solve(log=False):
    runtime = 0
    start_time = time.time()
    solution_count = 0

    best_solution = []
    best_value = 0

    while runtime < TIME_LIMIT:
        thesis_array = ThesisGreedy().solver()
        answer = ProfessorGreedy(thesis_array).solver()

        if answer:
            solution_count += 1
            prof_array, objective_value = answer
            if objective_value > best_value:
                best_value = objective_value
                best_solution = [thesis_array, prof_array]
        runtime = time.time() - start_time

    if best_value == 0:
        print("No solution founded")
        return

    print(num_thesis)
    for _ in best_solution[0]:
        print(best_solution[0][_], end=" ")
    print()
    print(num_prof)
    for _ in best_solution[1]:
        print(_, end=" ")

    if log:
        print()
        print(f'Optimal value: {best_value}')
        print(f'Total solution: {solution_count}')
        # Add sth here if you want to debug


solve(log=True)
