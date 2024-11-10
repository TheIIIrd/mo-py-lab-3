"""
Функции для итераций симплекс-метода:
- find_simplex_resolve: Находит разрешающий элемент в симплекс-методе и определяет условия для продолжения.
- find_min_ratio: Находит минимальное отношение для заданного столбца в симплекс-таблице.
- simplex_table_iteration: Выполняет одну итерацию симплекс-метода с обновлением коэффициентов и ограничений.
"""

from .checks import check_simplex_response


def find_simplex_resolve(c, A, b):
    """
    Находит разрешающий элемент в симплекс-методе.
    Возвращает информацию о минимальном отношении или специальные строки.
    """
    if check_simplex_response(c, A, b):
        # Проверяем, корректна ли симплекс-таблица

        for row in range(len(b)):
            if b[row] < 0:
                for col in range(len(A[0])):
                    if A[row][col] < 0:
                        # Возвращаем минимальное отношение для данного столбца
                        try:
                            return find_min_ratio(A, b, col)
                        except:
                            return ["inf"]

        c_max_value = max(c)
        if c_max_value < 0:
            # Если максимальное значение меньше нуля
            return ["not"]

        c_max_index = c.index(c_max_value)
        try:
            return find_min_ratio(A, b, c_max_index)
        except:
            return ["inf"]

    else:
        return ["not"]


def find_min_ratio(A, b, min_ratio_col):
    """
    Находит минимальное отношение для заданного столбца в симплекс-таблице.
    """
    min_ratio = float("inf")
    min_ratio_row = -1

    for row in range(len(A)):
        if A[row][min_ratio_col] == 0:
            continue

        ratio = b[row] / A[row][min_ratio_col]

        # Обновляем минимальное отношение, если нашли новое
        if (ratio > 0) and (ratio <= min_ratio):
            min_ratio = ratio
            min_ratio_row = row

    # Если не найден подходящий индекс, выбрасываем ошибку
    if min_ratio_row == -1:
        raise ValueError("[ ! ] Нет допустимого разрешающего элемента.")

    return [A[min_ratio_row][min_ratio_col], min_ratio_row, min_ratio_col]


def simplex_table_iteration(c, A, b, f, simplex_resolve):
    """
    Функция для выполнения одной итерации симплекс-метода.
    """
    # Получаем значение разрешающего элемента
    new_simplex_resolve = 1 / simplex_resolve[0]

    new_c = [0] * len(c)  # Инициализируем новый вектор коэффициентов целевой функции
    new_b = [0] * len(b)  # Инициализируем новый вектор правых частей
    new_A = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]  # Инициализируем новую матрицу ограничений

    # Заполняем колонну A
    for i in range(len(A)):
        if i == simplex_resolve[1]: # Текущая строка разрешающего элемента
            new_A[i][simplex_resolve[2]] = new_simplex_resolve
        else:                       # Остальные строки
            new_A[i][simplex_resolve[2]] = (
                A[i][simplex_resolve[2]] / simplex_resolve[0] * -1
            )

    # Обновляем коэффициенты целевой функции для разрешающего столбца
    new_c[simplex_resolve[2]] = c[simplex_resolve[2]] / simplex_resolve[0] * -1

    # Заполняем строку A для разрешающего элемента
    for i in range(len(A[0])):
        if i == simplex_resolve[2]:
            continue
        new_A[simplex_resolve[1]][i] = A[simplex_resolve[1]][i] / simplex_resolve[0]

    # Обновляем вектор правых частей для разрешающего элемента
    new_b[simplex_resolve[1]] = b[simplex_resolve[1]] / simplex_resolve[0]

    # Обновляем остальные коэффициенты целевой функции
    for i in range(len(c)):
        if i == simplex_resolve[2]:
            continue
        new_c[i] = (c[i] - (A[simplex_resolve[1]][i] * c[simplex_resolve[2]])
                   / simplex_resolve[0]
        )

    # Обновляем вектор правых частей для остальных строк
    for i in range(len(b)):
        if i == simplex_resolve[1]:
            continue
        new_b[i] = b[i] - (
            (A[i][simplex_resolve[2]] * b[simplex_resolve[1]])
            / simplex_resolve[0]
        )

    # Обновляем матрицу ограничений
    for i in range(len(A)):
        for j in range(len(A[0])):
            if (i == simplex_resolve[1]) or (j == simplex_resolve[2]):
                continue
            new_A[i][j] = A[i][j] - (
                (A[i][simplex_resolve[2]] * A[simplex_resolve[1]][j])
                / simplex_resolve[0]
            )

    # Обновляем значение целевой функции
    new_f = f - ((c[simplex_resolve[2]] * b[simplex_resolve[1]])
                / simplex_resolve[0])

    return new_c, new_A, new_b, new_f
