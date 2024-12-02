import numpy as np


# Функція для перевірки, чи є відношення асиметричним
def is_asymmetric(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1 and matrix[j][i] == 1:
                return False
    return True

# Функція для пошуку домінуючих альтернатив
def find_dominating_alternatives(matrix):
    print("\nОптимальні альтернативи за принципом домінування:")
    is_asymetric = is_asymmetric(matrix)
    
    if is_asymetric:
        print("Відношення асиметричне.")
        X_p = []
        for i in range(len(matrix)):
            for j, el in enumerate(matrix[i]):
                if i == j and el != 0:
                    break
                if i != j and el != 1:
                    break
            else:
                X_p.append(i + 1)
        print(f"X*P: {{{', '.join(map(str, X_p)) if X_p else '∅'}}}")
    else:
        print(f"Відношення не асиметричне")
        X_r = []
        for i in range(len(matrix)):
            if all(matrix[i]):
                X_r.append(i + 1)

        X__r = []
        for i in range(len(matrix)):
            if all(matrix[i]):
                for j in range(len(matrix)):
                    if i != j and matrix[j][i] == 1:
                        break
                else:
                    X__r.append(i + 1)
        print(f"X*R: {{{', '.join(map(str, X_r)) if X_r else '∅'}}}")
        print(f"X**R: {{{', '.join(map(str, X__r)) if X__r else '∅'}}}")

# Функція для пошуку блокованих альтернатив
def find_blocked_alternatives(matrix):
    print("\nОптимальні альтернативи за принципом блокування:")
    is_asymetric = is_asymmetric(matrix)
    
    if is_asymetric:
        print("Відношення асиметричне.")
        x_p = []
        for column_j in range(len(matrix[0])):
            for row_i in range(len(matrix)):
                if matrix[row_i][column_j] == 1:
                    break
            else:
                x_p.append(column_j + 1)
        print(f"X⁰P: {{{', '.join(map(str, x_p)) if x_p else '∅'}}}")
    else:
        print("Відношення не асиметричне")
        x_r = []
        for column_j in range(len(matrix[0])):
            for row_i in range(len(matrix)):
                if matrix[row_i][column_j] == 1 and matrix[column_j][row_i] == 0:
                    break
            else:
                x_r.append(column_j + 1)

        x__r = []
        for column_j in range(len(matrix[0])):
            for row_i in range(len(matrix)):
                if row_i != column_j and matrix[row_i][column_j] == 1:
                    break
            else:
                x__r.append(column_j + 1)
        print(f"X⁰R: {{{', '.join(map(str, x_r)) if x_r else '∅'}}}")
        print(f"X⁰⁰R: {{{', '.join(map(str, x__r)) if x__r else '∅'}}}")

# Приклад бінарних відношень R1 - R8 (матриці суміжності)
relations = {
    "R1": np.array([
        [1, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]),
    "R2": np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]),
    "R3": np.array([
        [0, 0, 1, 0, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 0, 1, 0, 0],
        [1, 1, 0, 0, 1, 1, 0, 0]
    ]),
    "R4": np.array([
        [1, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 1, 1, 0],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 1, 0, 1, 1, 1]
    ]),
    "R5": np.array([
        [1, 0, 0, 0, 1, 1, 1, 1],
        [0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 1]
    ]),
    "R6": np.array([
        [1, 0, 0, 1, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 1]
    ]),
    "R7": np.array([
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 1, 0],
        [1, 1, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0]
    ]),
    "R8": np.array([
        [0, 0, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
}

# Обробка кожного відношення
for name, relation in relations.items():
    print(f"\n{name}:")
    find_dominating_alternatives(relation)
    find_blocked_alternatives(relation)
    print()
