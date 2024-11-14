"""
Точка входа программы, инициирует параметры и запускает симплекс-метод.
"""

from simplexsus.simplexsus import simplexsus, to_dual_task
from simplexsus.bounds import branches_and_bounds


def main():
    """
    Точка входа программы - инициализация значений и вызов симплекс-метода.
    """
    minimize = False                            # Необходимость минимизации
    c = [7, 4, 3]                               # Коэффициенты целевой функции
    A = [[3, 1, 1], [1, 1, 0], [0, 0.5, 4]]     # Ограничения
    b = [5, 2, 6]                               # Правая часть ограничений
    f = 0                                       # Значение функции

    # c, A, b, minimize = to_dual_task(c, A, b, minimize)
    # print("\033[93m[ + ]\033[0m Answer:", simplexsus(c, A, b, f, minimize))
    print("\033[93m[ + ]\033[0m Best answer:", branches_and_bounds(c, A, b, f, minimize))

    return 0


if __name__ == "__main__":
    main()
