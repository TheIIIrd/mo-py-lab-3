"""
Функции для проверки входных данных:
- check_simplex_table: Проверяет корректность входных данных для симплекс-метода.
- check_simplex_response: Проверяет существование решения и возможность перехода к следующей итерации.
- check_simplex_answer: Проверяет корректность решения, полученного с использованием симплекс-метода.
"""

def check_simplex_table(c, A, b):
    """
    Проверка корректности входных данных для симплекс-метода.
    """
    len_A = len(A[0])  # Количество переменных

    # Проверяет, что все строки матрицы A имеют одинаковую длину
    # и содержат допустимые значения
    for row in A:
        if len(row) != len_A:
            return False  # Длина строки не соответствует ожидаемой

    # Проверяем, что длины векторов c и b соответствуют количеству строк в A
    if (len(c) != len_A) or (len(b) != len(A)):
        return False

    # Проверка пройдена успешно
    return True


def check_simplex_response(c, A, b):
    """
    Проверяет, существует ли решение симплекс-метода
    """
    if c.count(0) == len(c):
        return False  # Все коэффициенты равны нулю

    for row in range(len(b)):
        if b[row] < 0:                      # Если есть отрицательный элемент в b
            for col in range(len(A[0])):    # Ошибка в исходном коде: A должен быть матрицей
                if min(A[row]) >= 0:
                    return False            # Нет подходящих коэффициентов

    return True  # Существуют отрицательные коэффициенты


def check_simplex_answer(c, b, f, var_row, var_col):
    """
    Проверяет корректность решения, полученного с использованием симплекс-метода.
    """
    check_f = 0

    for i in range(len(var_row)):
        if var_row[i] in var_col:
            check_f += b[i] * c[var_col.index(var_row[i]) - 1]

    if round(check_f, 2) == round(f, 2):
        return True

    return False
