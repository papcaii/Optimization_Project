import random


def generate_test_case(file_path, N, M, K):
    with open(file_path, 'w') as inp_file:
        # Constraints
        a = random.randint(2, N // K - 1)
        b = random.randint(a + 1, min(2 * a, N))
        c = random.randint(1, M // K - 1)
        d = random.randint(c + 1, min(2 * c, M))
        e = random.randint(1, 2)
        f = random.randint(1, 2)

        # Matrix s (similarity between projects)
        s_matrix = [[0 if i == j else random.randint(1, 5) for j in range(N)] for i in range(N)]

        # Make s_matrix symmetric
        for i in range(N):
            for j in range(i + 1, N):
                s_matrix[j][i] = s_matrix[i][j]

        # Matrix g (similarity between projects and teachers)
        g_matrix = [[random.randint(1, 5) for _ in range(M)] for _ in range(N)]

        # List of teachers guiding each project
        teachers = [random.randint(1, M) for _ in range(N)]

        # Write to the file
        inp_file.write(f"{N} {M} {K}\n")
        inp_file.write(f"{a} {b} {c} {d} {e} {f}\n")

        for row in s_matrix:
            inp_file.write(" ".join(map(str, row)) + "\n")

        for row in g_matrix:
            inp_file.write(" ".join(map(str, row)) + "\n")

        inp_file.write(" ".join(map(str, teachers)))
        print("DONE !")


# Input values for N, M, K from the user
N = int(input("Enter the number of theses: "))
M = int(input("Enter the number of professor: "))
K = int(input("Enter the number of council: "))

# Generate a test case and write to the data.inp file
generate_test_case("data.inp", N, M, K)
