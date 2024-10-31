"""
Вспомогательные функции:
- to_dual_task: Преобразует заданные параметры для двойственной задачи линейного программирования.
- swap_variables: Меняет местами элементы в списках переменных на основе разрешающего элемента.
"""


def to_dual_task(c, A, b, minimize):
    """
    Преобразует заданные параметры для двойственной задачи линейного программирования.
    """
    new_c = b.copy()
    new_b = [-elem for elem in c]

    # Создаем новую матрицу A для двойственной задачи
    # Размерность new_A: количество столбцов A x количество строк A
    new_A = [[0 for _ in range(len(A))] for _ in range(len(A[0]))]

    # Заполняем новую матрицу A, транспонируя оригинальную матрицу A
    for row in range(len(A)):
        for col in range(len(A[0])):
            new_A[col][row] = A[row][col] * -1

    return new_c, new_A, new_b, not minimize


def swap_variables(var_row, var_col, simplex_resolve):
    """
    Меняет местами элементы в двух списках на основе указаний,
    полученных из решения симплекс-метода.
    """
    var_row[simplex_resolve[1]], var_col[simplex_resolve[2] + 1] = (
        var_col[simplex_resolve[2] + 1],
        var_row[simplex_resolve[1]],
    )

    return var_row, var_col
