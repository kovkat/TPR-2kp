import numpy as np
from tabulate import tabulate

def is_cyclic(matrix):
    def has_cycle(node, visited, stack, current_cycle):
        visited[node] = True
        stack[node] = True
        current_cycle.append(node)

        for neighbor in range(len(matrix)):
            if matrix[node][neighbor] == 1:
                if not visited[neighbor]:
                    if has_cycle(neighbor, visited, stack, current_cycle):
                        return True
                elif stack[neighbor]:
                    cycle_start = current_cycle.index(neighbor)
                    cycle = current_cycle[cycle_start:] + [neighbor]
                    print("\nЦикл:", " => ".join(map(str, map(lambda x: x + 1, cycle))))
                    return True

        stack[node] = False
        current_cycle.pop()
        return False

    visited = [False] * len(matrix)
    stack = [False] * len(matrix)

    for node in range(len(matrix)):
        if not visited[node]:
            if has_cycle(node, visited, stack, []):
                return True  # Цикл знайдено

    return False  # Циклу немає





def neyman_morgenshtern(matrix):
    # шукаємо елементи, в яких верхній переріз порожній це буде перша множина S0/ для цього в стовпчику мають бути всі 0
    S0=set()
    n = len(matrix)
    for el in range(n):
        best = True 
        for j in range(n):
            if matrix[j][el] == 1:
                best = False
                break
        if best:
            S0.add(el+1)
    print("\nКРОК 1. Множина S")
    # Шукаємо переріз множин Sk/Sk-1 / ті елементи , де у верхньому перерізі присутні лише елементи множини Sk-1
    S_set = [("S0", S0)]
    Sk_k1 = [] #переріз множин Sk/Sk-1
    i = 0
    prev = S0 # попередня множина 
 
    while len(S_set[-1][1])  != n: #будемо виконувати алгоритм , допоки всі елементи не будуть присутні в цій множині
        i +=1
        Sk = set() #поточна множина
        for el in range(n):
            for j in range(n):
                if matrix[j][el] == 1 and ((j + 1) not in prev): #ця умова для того, щоб відкинути елементи, в яких у верхньому перерізі є елементи не з множини Sk 
                    break
            else :
                Sk.add(el+1)
        diff = Sk.difference(prev)
        Sk_k1.append((f"S{i}/S{i-1}",diff))
        S_set.append((f"S{i}", Sk))
        prev = Sk

    # Вивід результатів 
    headers = ["Si", "Result"]  # Заголовки стовпців
    Sk_k1_table = [(("S0", ' '.join(map(str, S0))))]  # Додаємо перший елемент S0
    Sk_k1_table.extend([(set_, ' '.join(map(str, diff))) for set_, diff in Sk_k1])
    table = tabulate(Sk_k1_table, headers=headers, tablefmt="pretty")
    print(table)
    
    print("\nКРОК 2. Множина Q")
    Q0 = S0.copy() #Q0 = S0
    Q_set = [("Q0", Q0)]

    # Множину Q ми створюємо на основі кроку 1 Sk\k-1
    # Елементи множини Sk\k-1 є кандидатами множини Qk, для того , щоб стати її елементами, то має виконуватися умова:
    # Верхній переріз кандидату з множиною Qk-1 немає мати спільних елементів
    for l, (set_, diff_) in enumerate( Sk_k1, start=1):
        Qk = set()  # Створюємо порожню множину Q
        for el in diff_: #Перебираємо кандидатів
            R_ = set() #верхній переріз (стовпець)
            for j in range(n):
                if matrix[j][el -1] == 1:
                    R_.add(j+1)
            #Перевіряємо кадидатів
            if len( R_.intersection(Q_set[-1][1]))==0:
                Qk.add(el)
        Q_set.append((f"Q{l}", Q_set[-1][1].union(Qk)))

    #Вивід таблиці для кроку 2
    headers = ["Ri", "Result"]  # Заголовки стовпців
    Qi_table=([(set_, ' '.join(map(str, diff))) for set_, diff in Q_set])
    table = tabulate(Qi_table, headers=headers, tablefmt="pretty")
    print(table)

    X_HM = Q_set[-1][1]
    print(f"Розвʼязок Неймана-Моргенштерна {X_HM = }")

    #print("\nПеревірка внутріншьої стійкості:\n")
    for column_id in X_HM:
        for row_id in X_HM:
            if matrix[row_id - 1][column_id - 1] == 1:
                print(
                    f"\nЕлемент ({row_id}, {column_id}) = 1. Внутрішня  стійкість: ні.")
                break
            #else:
            #print(f"({row_id}, {column_id}) = {matrix[row_id - 1][column_id - 1]}")
        if matrix[row_id - 1][column_id - 1] == 1:
            break
    else:
        print("\nВнутрішня стійкість: так")

    #print("\nПеревірка зовнішньої стійкості:\n")
    not_in_X_HM = set(range(1, n + 1)) - X_HM

    for column_id in not_in_X_HM:
        for row_id in X_HM:
            if matrix[row_id - 1][column_id - 1] == 1:
                #print(f"У елемента {column_id} є вхідний зв'язок з вершини {row_id}. ")
                break
        else:
            #print(f"\nЕлемент {column_id} не має вхідних зв'язків з вершин {X_HM}! Перевірку не пройдено.")
            print("\nЗовнішння стійкість: ні")
            break
    else:
        print("\nЗовнішння стійкість: так")


   


def transform_matrix(matrix):
    print("PIN-вигляд")
    n = len(matrix)
    new_matrix = [["0" for _ in range(n)] for _ in range(n)]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0 and matrix[j][i] == 1:
                new_matrix[j][i] = "P"
            if matrix[i][j] == 1 and matrix[j][i] == 0:
                new_matrix[i][j] = "P"
            if matrix[i][j] == 1 and matrix[j][i] == 1:
                new_matrix[i][j], new_matrix[j][i] = "I", "I"
            if matrix[i][j] == 0 and matrix[j][i] == 0:
                new_matrix[i][j], new_matrix[j][i] = "N", "N"
    
    for row in new_matrix:
        print(" ".join(row))
    
    return new_matrix


def k_optimization(matrix):

    # Перетворюємо матрицю до PIN-вигляду
    pin_matrix = transform_matrix(matrix)

    types = ["P_I_N", "P_N", "P_I", "P"]  

    # Проходимо кожен сценарій
    for k, type in enumerate(types, start=1):
        print(f"\nK-{k} оптимізація ({type}), множина S{k}(x):")

        # Створення множин S_k(x) для кожного рядка
        S_k_set = [
            {j + 1 for j, elem in enumerate(row) if elem in type}
            for row in pin_matrix
        ]
      
         # Побудова матриці S_k(x)
        S_k_matrix = [
            [1 if elem in type else 0 for elem in row] for row in pin_matrix
        ]

        # Виведення матриці S_k(x)
        print(f"Матриця S{k}(x):")
        for row in S_k_matrix:
            print(" ".join(map(str, row)))

        # Формуємо K-max множину (рядки, що є надмножинами для всіх інших)
        k_max_set = {
            i + 1 for i, s_k in enumerate(S_k_set)
            if all(s_k.issuperset(other) for other in S_k_set)
        }
        print(f"{k}-max: {k_max_set if k_max_set else '{∅}'}")

        # Формуємо K-opt множину (рядки, які включають усі альтернативи)
        k_opt_set = {
            i + 1 for i, s_k in enumerate(S_k_set) if len(s_k) == len(matrix)
        }

        print(f"{k}-opt: {k_opt_set if k_opt_set else '{∅}'}")

    


def solve(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))
    if is_cyclic(matrix):
        print("Циклічне. Оптимізація за принципом К-оптимізації.\n")
        k_optimization(matrix)
    else:
        print("Ациклічне. Оптимізація за Нейманом-Моргенштерном")
        neyman_morgenshtern(matrix)
    print()

relations = {
    "R1": np.array([
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    ]),
    "R2": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1]
    ]),
    "R3": np.array([
         [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    "R4": np.array([
        [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    ]),
    "R5": np.array([
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    ]),
    "R6": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    "R7": np.array([
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    "R8": np.array([
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    ]),
    "R9": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    "R10": np.array([
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
}

for name, relation in relations.items():
    print(f"\n{name}:")
    solve(relation)
    print("-" * 13)

