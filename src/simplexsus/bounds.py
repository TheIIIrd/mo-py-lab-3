"""
Модуль для реализации метода ветвей и границ (Branch and Bound) для нахождения
целочисленных решений задач линейного программирования.

Методы:

1. branches_and_bounds(c, A, b, f, minimize, best_solution=None):
   - Реализует метод ветвей и границ для нахождения целочисленного решения
     задачи линейного программирования.
   - Возвращает лучшую найденную целочисленную оптимизацию в виде списка,
     содержащего оптимальное значение целевой функции и значения переменных.

2. check_integer_solution(answer_simplexsus, answer_variables, best_solution):
   - Проверяет, является ли текущее решение целочисленным, и обновляет лучшее
     решение, если текущее решение лучше.
   - Возвращает обновленное лучшее решение, если текущее решение целочисленное
     и лучшее, иначе возвращает текущее лучшее решение.

3. check_best_solution(c, A, b, minimize, best_solution):
   - Проверяет, является ли текущее решение лучшим, с учетом ограничений.
   - Перебирает все возможные значения переменных в заданных пределах и
     вычисляет целевую функцию для каждой комбинации.
   - Возвращает True, если найдено решение, удовлетворяющее ограничениям,
     иначе False.

4. is_integer(value):
   - Проверяет, является ли переданное значение целым числом.
   - Возвращает True, если значение является целым числом, иначе False.
"""

from .simplexsus import simplexsus
from math import floor


def branches_and_bounds(c, A, b, f, minimize, best_solution=None):
    """
    Реализация метода ветвей и границ для нахождения целочисленного решения задачи линейного программирования.
    """
    stack = [(c, A, b, f, minimize, best_solution)]

    while stack:
        (
            current_c,
            current_A,
            current_b,
            current_f,
            current_minimize,
            current_best_solution,
        ) = stack.pop()

        answer_simplexsus = simplexsus(current_c, current_A, current_b, current_f, current_minimize)

        if answer_simplexsus[0] == float("inf"):
            continue  # Нет решения, пропускаем итерацию

        answer_variables = answer_simplexsus[1::]
        current_best_solution = check_integer_solution(answer_simplexsus, answer_variables, current_best_solution, minimize)

        # Если нашли новое лучшее решение, обновляем best_solution
        if current_best_solution is not None and (best_solution is None or current_best_solution[0] > best_solution[0]):
            best_solution = current_best_solution

        i = 0
        found = False
        while i < len(answer_variables) and not found:
            if not is_integer(answer_variables[i]):
                # Ветвление
                branching_variable = floor(answer_variables[i])

                print(
                    f"\n\033[95m[ * ]\033[0m Adding a new condition for x{i + 1} = {answer_variables[i]}:",
                    f"\033[95m[x{i + 1} <= {branching_variable}; x{i + 1} >= {branching_variable + 1}]\033[0m\n",
                )

                # Создаем новые ограничения
                new_A_left = current_A + [[0 if j != i else 1 for j in range(len(c))]]
                new_b_left = current_b + [branching_variable]

                # Добавляем новое ограничение для x_i <= branching_variable
                stack.append(
                    (
                        current_c,
                        new_A_left,
                        new_b_left,
                        current_f,
                        current_minimize,
                        best_solution,
                    )
                )

                # Добавляем ограничение для x_i >= branching_variable + 1
                new_A_right = current_A + [[0 if j != i else -1 for j in range(len(c))]]
                new_b_right = current_b + [(branching_variable + 1) * -1]

                stack.append(
                    (
                        current_c,
                        new_A_right,
                        new_b_right,
                        current_f,
                        current_minimize,
                        best_solution,
                    )
                )

                found = True  # Устанавливаем флаг, чтобы выйти из цикла

            i += 1  # Увеличиваем индекс

    if check_best_solution(c, A, b, minimize, best_solution):
        return best_solution
    else:
        return [float("inf")]


def check_integer_solution(answer_simplexsus, answer_variables, best_solution, minimize):
    """
    Проверяет, является ли текущее решение целочисленным и обновляет лучшее решение.
    """
    is_integer_solution = all(floor(var) == var for var in answer_variables)

    if is_integer_solution:
        if best_solution is None or (minimize and answer_simplexsus[0] < best_solution[0]):
            best_solution = answer_simplexsus

            print(
                "\033[93m[ + ]\033[0m New best solution found:\033[93m",
                best_solution,
                "\033[0m\n",
            )

        elif (not minimize) and answer_simplexsus[0] > best_solution[0]:
            best_solution = answer_simplexsus

            print(
                "\033[93m[ + ]\033[0m New best solution found:\033[93m",
                best_solution,
                "\033[0m\n",
            )

        else:
            print(
                "\033[95m[ * ]\033[0m Current solution is integer but not better:\033[93m",
                answer_simplexsus,
                "\033[0m\n",
            )

    return best_solution


def check_best_solution(c, A, b, minimize, best_solution):
    """
    Проверяет, является ли текущее решение лучшим, с учетом ограничений.
    """
    # Определяем ограничение по максимальному значению из вектора b
    limitation = floor(max(b)) + 1

    # Инициализируем список альтернативных значений переменных с нулями
    x_alternatives = [0 for _ in c]

    # Определяем количество цифр в целевой функции для форматирования вывода
    num_digits_f = len(str(abs(best_solution[0])))

    if len(x_alternatives) == 3:
        for x_alternatives[0] in range(limitation):
            for x_alternatives[1] in range(limitation):
                for x_alternatives[2] in range(limitation):
                    check_f = sum(c[i] * x_alternatives[i] for i in range(len(c)))

                    # Выводим текущее состояние перебора
                    print(
                        f"\033[95m[ * ]\033[0m Scrambling... {x_alternatives} F = {check_f}:",
                        end=(" " * (num_digits_f - len(str(abs(check_f))))),
                    )

                    # Проверка ограничений
                    row = 0
                    len_A = len(A)
                    constraint_check = True

                    # Проверяем каждое ограничение
                    while row < len_A and constraint_check:
                        check_row = sum(A[row][col] * x_alternatives[col] for col in range(len(A[0])))
                        constraint_check = round(check_row, 1) <= round(b[row], 1)
                        constraint_result = "\033[92m[True]\033[0m" if constraint_check else "\033[91m[False]\033[0m"

                        row += 1

                    print(constraint_result)

                    # Если текущее значение не удовлетворяет ограничениям, продолжаем
                    if not constraint_check:
                        continue

                    # Если мы не минимизируем и текущее значение целевой функции больше, чем лучшее решение, выводим сообщение
                    elif not minimize and check_f > best_solution[0]:
                        print(
                            f"\n\033[91m[ - ] There's no answer\033[0m: {[check_f] + x_alternatives}"
                        )
                        return False

                    # Если мы минимизируем и текущее значение целевой функции меньше, чем лучшее решение, выводим сообщение
                    elif minimize and check_f < best_solution[0]:
                        print(
                            f"\n\033[91m[ - ] There's no answer\033[0m: {[check_f] + x_alternatives}"
                        )
                        return False

                    # Если текущее значение целевой функции равно лучшему решению, но альтернативы отличаются, выводим сообщение
                    elif check_f == best_solution[0] and x_alternatives != best_solution[1::]:
                        print(
                            f"\033[93m[ + ]\033[0m Yet another answer found: {[check_f] + x_alternatives}"
                        )

    print()
    return True  # Возвращаем True, если все проверки пройдены


def is_integer(value):
    """
    Проверяет, является ли значение целым числом.
    """
    return floor(value) == value
