"""
Функции для работы с симплекс-таблицей:
- create_simplex_table: Создает симплекс-таблицу из заданных коэффициентов, ограничений и правых частей.
- create_simplex_variables: Создает имена переменных для симплекс-таблицы.
- print_simplex_table: Выводит симплекс-таблицу в консоль в форматированном виде.
"""

def create_simplex_table(c, A, b, f):
    """
    Создает симплекс-таблицу из коэффициентов c, матрицы A и вектора b и f.
    """
    table = []
    rounded_c = [round(elem, 2) for elem in c]
    rounded_A = [[round(elem, 2) for elem in row] for row in A]

    # Формируем таблицу, добавляя строки с b и A
    for i in range(len(A)):
        table.append([round(b[i], 2)] + rounded_A[i])

    # Добавляем строку с коэффициентами c
    table.append([round(f, 2)] + rounded_c)

    return table


def create_simplex_variables(A):
    """
    Создает имена переменных для метода симплекс-метода.
    """
    var_col = ["b"] + [f"x{i+1}" for i in range(len(A[0]))]
    var_row = [f"x{i+1+len(var_col)}" for i in range(len(A))] + ["F "]
    return var_row, var_col


def print_simplex_table(simplex_table, var_row, var_col):
    """
    Выводит симплекс-таблицу в терминал с заголовками.
    """
    print()

    # Определяем максимальную ширину для форматирования
    max_width = max(len(str(float(j))) for row in simplex_table for j in row) + 2

    # Выводим заголовки
    headers = [var_col[i] for i in range(len(simplex_table[0]))]
    print("    ", " | ".join(f"{header:>{max_width}}" for header in headers))
    print("----", "-" * (max_width * len(headers) + 4 * (len(headers) - 1)), sep="")

    for i in range(len(simplex_table)):
        print(var_row[i], end=" | ")

        for j in simplex_table[i]:
            # Выравнивание по правому краю, 2 знака после запятой
            if j == 0:
                print(f"{float(0):>{max_width}.2f}", end=" | ")
            else:
                print(f"{float(j):>{max_width}.2f}", end=" | ")
        print()

    return
