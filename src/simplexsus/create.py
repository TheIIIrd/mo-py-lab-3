"""
Функции для работы с симплекс-таблицей:
- create_simplex_table: Создает симплекс-таблицу из заданных коэффициентов, ограничений и правых частей.
- create_simplex_variables: Создает имена переменных для симплекс-таблицы.
- create_answer_variables: Создает искомый вектор значений в форматированном виде.
"""


def create_simplex_table(c, A, b, f):
    """
    Создает симплекс-таблицу из коэффициентов c, матрицы A и вектора b и f.
    """
    table = []
    rounded_c = [round(num, 2) for num in c]
    rounded_A = [[round(num, 2) for num in row] for row in A]

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


def create_answer_variables(b, var_row, old_var_col):
    """
    Создает искомый вектор значений
    """
    answer_variables = [0 for _ in range(len(old_var_col) - 1)]

    for i in range(len(var_row)):
        if var_row[i] in old_var_col:
            # Сохранение значения
            answer_variables[old_var_col.index(var_row[i]) - 1] = round(b[i], 2)

    return answer_variables
