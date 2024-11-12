"""
Программа реализует симплекс-метод для решения задач линейного программирования.
Содержит функции для проверки входных данных, создания симплекс-таблицы,
поиска разрешающего элемента, выполнения итераций симплекс-метода, преобразования
в двойственную задачу и вывода результатов на экран.

Функции:
- simplexsus: Основная функция симплекс-метода, выполняет проверку данных и находит оптимальное решение.

Для использования достаточно задать коэффициенты целевой функции, ограничения и правые части.
Результатом будет оптимальное значение целевой функции и соответствующие решения переменных.
"""

from .checks import *
from .create import *
from .iterations import *
from .utils import *
from .write import *


def simplexsus(c, A, b, f, minimize):
    """
    Основная функция симплекс-метода. Выполняет проверку входных данных
    и находит решение.
    """
    # Проверка условий
    if check_simplex_table(c, A, b):
        print("[ + ] Check: OK")
        old_c = c.copy()
        old_A = A.copy()
        old_b = b.copy()

        # Инвертируем c, если ищем минимум
        if minimize:
            c = [-elem for elem in c]

        var_row, var_col = create_simplex_variables(A)  # Создание обозначений симплекс-таблицы
        old_var_row = var_row.copy()
        old_var_col = var_col.copy()

        while (max(c) > 0) or (min(b) < 0):
            simplex_table = create_simplex_table(c, A, b, f)        # Создание симплекс-таблицы
            print_simplex_table(simplex_table, var_row, var_col)    # Вывод симплекс-таблицы
            simplex_resolve = find_simplex_resolve(c, A, b)         # Поиск и выбор разрешающего элемента

            # Обработка результатов нахождения разрешающего элемента
            if simplex_resolve == ["not"]:
                print("[ - ] There's no answer")
                return [float("inf")]
            if simplex_resolve == ["inf"]:
                print("[ - ] Infinite number of solutions")
                return [float("inf")]

            print(
                "[ * ] The resolving element is found:",
                round(simplex_resolve[0], 2),
                simplex_resolve[1:],
            )

            var_row, var_col = swap_variables(var_row, var_col, simplex_resolve)
            c, A, b, f = simplex_table_iteration(c, A, b, f, simplex_resolve)

        # Найдено оптимальное решение
        print("\n[ + ] OPTI ANS", end="")
        simplex_table = create_simplex_table(c, A, b, f)        # Создание симплекс-таблицы
        print_simplex_table(simplex_table, var_row, var_col)    # Вывод симплекс-таблицы

    else:
        print("[ - ] Check: BAD TABLE")
        return [float("inf")]

    if not minimize:
        f *= -1

    if print_simplex_answer(old_c, old_A, old_b, b, f, var_row, old_var_col):
        answer_variables = create_answer_variables(b, var_row, old_var_col)

        if minimize:
            print("[ * ] F -> minimum")
            return [round(f, 2)] + answer_variables
        else:
            print("[ * ] F -> maximum")
            return [round(f, 2)] + answer_variables

    print("[ - ] Check: BAD ANS")
    return [float("inf")]
