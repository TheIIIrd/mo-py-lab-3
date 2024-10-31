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


def print_simplex_answer(c, A, b, f, var_row, var_col):
    """
    Выводит решение с проверкой симплекс-таблицы в терминал.
    """
    answer_variables = [0 for _ in range(len(var_col) - 1)]
    print_data = ["\nF = "]
    check_f = 0

    for i in range(len(var_row)):
        if var_row[i] in var_col:
            answer_variables[var_col.index(var_row[i]) - 1] = round(b[i], 2)
            check_f += b[i] * c[var_col.index(var_row[i]) - 1]

            print_data += ["( ", round(b[i], 2), " * ", c[var_col.index(var_row[i]) - 1], " )", " + "]

    print_data.pop()
    print_data.append("\n")

    if round(check_f, 2) == round(f, 2):
        for row in range(len(A)):
            check_row = 0

            for col in range(len(A[0])):
                check_row += A[row][col] * answer_variables[col]
                print_data += ["( ", round(A[row][col], 2), " * ", answer_variables[col], " )", " + "]

            print_data.pop()
            print_data += [" <= ", round(b[row], 2)]

            if round(check_row, 2) <= b[row]:
                print_data += [" True", "\n"]

            else:
                print_data += [" False", "\n"]

                for element in print_data:
                    print(element, sep="", end="")
                print()

                return False

        for element in print_data:
            print(element, sep="", end="")
        print("\n[ * ] ", end="")

        for i in range(len(answer_variables)):
            print(f"x{i} = {answer_variables[i]}", end=" ")
        print()

    else:
        return False

    return True
