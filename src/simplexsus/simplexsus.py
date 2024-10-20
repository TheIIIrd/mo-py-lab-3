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
from .simplex_table import *
from .iterations import *
from .utils import *


def simplexsus(c, A, b, f, minimize):
    """
    Основная функция симплекс-метода. Выполняет проверку входных данных
    и находит решение.
    """
    # Проверка условий
    if check_simplex_table(c, A, b):
        print("[ + ] Check: OK")
        old_b = b.copy()

        # Инвертируем c, если ищем минимум
        if minimize:
            for i in range(len(c)):
                c[i] *= -1

        var_row, var_col = create_simplex_variables(A)  # Создание обозначений симплекс-таблицы
        old_var_row = var_row.copy()

        while (max(c) > 0) or (min(b) < 0):
            simplex_table = create_simplex_table(c, A, b, f)        # Создание симплекс-таблицы
            print_simplex_table(simplex_table, var_row, var_col)    # Вывод симплекс-таблицы
            simplex_resolve = find_simplex_resolve(c, A, b)         # Поиск и выбор разрешающего элемента

            # Обработка результатов нахождения разрешающего элемента
            if simplex_resolve == ["not"]:
                print("[ - ] There's no answer")
                return 1
            if simplex_resolve == ["inf"]:
                print("[ - ] Infinite number of solutions")
                return 1

            print("[ * ] The resolving element is found:", round(simplex_resolve[0], 2), simplex_resolve[1:])

            var_row, var_col = swap_variables(var_row, var_col, simplex_resolve)
            c, A, b, f = simplex_table_iteration(c, A, b, f, simplex_resolve)

        # Найдено оптимальное решение
        print("\n[ + ] OPTI ANS", end="")
        simplex_table = create_simplex_table(c, A, b, f)        # Создание симплекс-таблицы
        print_simplex_table(simplex_table, var_row, var_col)    # Вывод симплекс-таблицы

    else:
        print("[ - ] Check: BAD TABLE")
        return 1

    if check_simplex_answer(c, old_b, f, old_var_row, var_col):
        if minimize:
            print("[ * ] The function goes to the minimum")
            return round(f, 2)

        else:
            print("[ * ] The function goes to the maximum")
            return round(f * -1, 2)

    print("[ - ] Check: BAD ANS")
    return -1
