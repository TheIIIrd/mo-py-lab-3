"""
Функции для работы с симплекс-таблицей:
- print_simplex_table: Выводит симплекс-таблицу в консоль в форматированном виде.
- print_simplex_answer: Выводит решение с проверкой симплекс-таблицы.
"""

from .create import create_answer_variables


def print_simplex_table(simplex_table, var_row, var_col):
    """
    Выводит симплекс-таблицу в терминал с заголовками.
    """
    print()

    # Определяем максимальную ширину для форматирования
    max_width = max(len(str(float(j))) for row in simplex_table for j in row) + 2
    max_width_row = max(len(x) for x in var_row)

    # Выводим заголовки
    headers = [var_col[i] for i in range(len(simplex_table[0]))]
    print("    ", " | ".join(f"{header:>{max_width}}" for header in headers))
    print(
        "----",
        "-" * (max_width * len(headers) + 4 * (len(headers) - 1)),
        "-" * (max_width_row - 2),
        sep="",
    )

    for i in range(len(simplex_table)):
        print((var_row[i] + " " * (max_width_row - len(var_row[i]) + 1)), end="| ")

        for j in simplex_table[i]:
            # Выравнивание по правому краю, 2 знака после запятой
            if j == 0:
                print(f"{float(0):>{max_width}.2f}", end=" | ")
            else:
                print(f"{float(j):>{max_width}.2f}", end=" | ")
        print()

    return


def print_simplex_answer(old_c, old_A, old_b, b, f, var_row, old_var_col):
    """
    Выводит решение с проверкой симплекс-таблицы в терминал.
    """
    answer_variables = create_answer_variables(b, var_row, old_var_col)
    check_f = sum(
        b[i] * old_c[old_var_col.index(var_row[i]) - 1]
        for i in range(len(var_row))
        if var_row[i] in old_var_col
    )

    print(
        f"\nF = {' + '.join(f'({round(b[i], 2)} * {old_c[old_var_col.index(var_row[i]) - 1]})' for i in range(len(var_row)) if var_row[i] in old_var_col)}"
    )

    if round(check_f, 2) != round(f, 2):
        return False

    # Проверка ограничений
    for row in range(len(old_A)):
        check_row = sum(
            old_A[row][col] * answer_variables[col] for col in range(len(old_A[0]))
        )
        constraint_check = round(check_row, 1) <= round(old_b[row], 1)

        constraint_result = "[True]" if constraint_check else "[False]"
        print(
            f"{constraint_result} {' + '.join(f'({round(old_A[row][col], 2)} * {answer_variables[col]})' for col in range(len(old_A[0])))} <= {round(old_b[row], 2)}"
        )

        if not constraint_check:
            return False

    print(
        "\n[ * ]",
        "".join(
            f"x{i + 1} = {answer_variables[i]} " for i in range(len(answer_variables))
        ),
    )
    return True  # Успешное завершение
