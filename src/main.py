"""
Точка входа программы, инициирует параметры и запускает симплекс-метод.
"""

from simplexsus.simplexsus import simplexsus, to_dual_task


def main():
    """
    Точка входа программы - инициализация значений и вызов симплекс-метода.
    """
    minimize = False                            # Необходимость минимизации
    c = [7, 4, 3]                               # Коэффициенты целевой функции
    A = [[3, 1, 1], [1, 1, 0], [0, 0.5, 4]]     # Ограничения
    b = [5, 2, 6]                               # Правая часть ограничений
    f = 0

    c, A, b, minimize = to_dual_task(c, A, b, minimize)
    print("[ + ] Ans:", simplexsus(c, A, b, f, minimize))

    return 0


if __name__ == "__main__":
    main()
