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

3. is_integer(value):
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
        current_c, current_A, current_b, current_f, current_minimize, current_best_solution = stack.pop()

        answer_simplexsus = simplexsus(current_c, current_A, current_b, current_f, current_minimize)

        if answer_simplexsus[0] == float("inf"):
            continue  # Нет решения, пропускаем итерацию

        answer_variables = answer_simplexsus[1::]
        current_best_solution = check_integer_solution(answer_simplexsus, answer_variables, current_best_solution)

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
                    f"\n[ * ] Adding a new condition for x{i + 1} = {answer_variables[i]}:",
                    f"x{i + 1} <= {branching_variable}; x{i + 1} >= {branching_variable + 1}",
                )

                # Создаем новые ограничения
                new_A_left = current_A + [[0 if j != i else 1 for j in range(len(c))]]
                new_b_left = current_b + [branching_variable]

                # Добавляем новое ограничение для x_i <= branching_variable
                stack.append((current_c, new_A_left, new_b_left, current_f, current_minimize, best_solution))

                # Добавляем ограничение для x_i >= branching_variable + 1
                new_A_right = current_A + [[0 if j != i else -1 for j in range(len(c))]]
                new_b_right = current_b + [(branching_variable + 1) * -1]

                stack.append((current_c, new_A_right, new_b_right, current_f, current_minimize, best_solution))

                found = True  # Устанавливаем флаг, чтобы выйти из цикла

            i += 1  # Увеличиваем индекс

    return best_solution


def check_integer_solution(answer_simplexsus, answer_variables, best_solution):
    """
    Проверяет, является ли текущее решение целочисленным и обновляет лучшее решение.
    """
    is_integer_solution = all(floor(var) == var for var in answer_variables)

    if is_integer_solution:
        if best_solution is None or answer_simplexsus[0] < best_solution[0]:
            best_solution = answer_simplexsus
            print("[ + ] New best solution found:", best_solution, "\n")
        else:
            print("[ * ] Current solution is integer but not better:", answer_simplexsus)

    return best_solution


def is_integer(value):
    """
    Проверяет, является ли значение целым числом.
    """
    return floor(value) == value
