"""
Функции для работы с симплекс-таблицей:
- print_simplex_table: Выводит симплекс-таблицу в консоль в форматированном виде.
- print_simplex_answer: Выводит решение с проверкой симплекс-таблицы.
"""


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


def print_simplex_answer(old_c, old_A, old_b, b, f, var_row, old_var_col):
    """
    Выводит решение с проверкой симплекс-таблицы в терминал.
    """
    answer_variables = [0 for _ in range(len(old_var_col) - 1)]
    check_f = 0
    data = ["\nF = "]

    for i in range(len(var_row)):
        if var_row[i] in old_var_col:
            answer_variables[old_var_col.index(var_row[i]) - 1] = round(b[i], 2)    # Сохранение значения
            check_f += (b[i] * old_c[old_var_col.index(var_row[i]) - 1])            # Подсчёт вклада в целевую функцию

            data += ["( ", round(b[i], 2), " * ", old_c[old_var_col.index(var_row[i]) - 1], " )", " + " ]

    data.pop()          # Удаление лишнего "+"
    data.append("\n")   # Новая строка

    if round(check_f, 2) == round(f, 2):    # Новая строка
        for row in range(len(old_A)):
            check_row = 0

            for col in range(len(old_A[0])):
                check_row += old_A[row][col] * answer_variables[col]
                data += ["( ", round(old_A[row][col], 2), " * ", answer_variables[col], " )", " + "]

            data.pop()
            data += [" <= ", round(old_b[row], 2)]

            # Проверка ограничений
            if (round(check_row, 2) <= (old_b[row] - 0.01)) or (
                round(check_row, 2) <= (old_b[row] + 0.01)
            ):
                data += [" True", "\n"]

            else:
                data += [" False", "\n"]

                for element in data:
                    print(element, sep="", end="")
                print()

                return False

        for element in data:
            print(element, sep="", end="")
        print("\n[ * ] ", end="")

        for i in range(len(answer_variables)):
            print(f"x{i+1} = {answer_variables[i]}", end=" ")
        print()

    else:
        return False

    return True  # Успешное завершение
