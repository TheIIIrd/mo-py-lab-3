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

4. branch_and_bound(c, A, b, f, minimize, answer_variables, i, best_solution):
   - Создает новое ограничение для ветвления и рекурсивно вызывает метод ветвей и границ.
   - Возвращает обновленное лучшее решение после выполнения ветвления.
"""

from .simplexsus import simplexsus
from math import floor


def branches_and_bounds(c, A, b, f, minimize, best_solution=None):
    """
    Реализация метода ветвей и границ для нахождения целочисленного решения задачи линейного программирования.
    """
    answer_simplexsus = simplexsus(c, A, b, f, minimize)
    print("[ * ] Ans:", answer_simplexsus)

    if answer_simplexsus[0] == float("inf"):
        print("[ - ] No solution")
        return best_solution  # Возвращаем текущее лучшее решение, а не [inf]

    answer_variables = answer_simplexsus[1::]
    best_solution = check_integer_solution(answer_simplexsus, answer_variables, best_solution)

    for i in range(len(answer_variables)):
        if not is_integer(answer_variables[i]):
            print("[ - ] Non-integer answer:", answer_simplexsus, "\n")
            best_solution = branch_and_bound(
                c, A, b, f, minimize, answer_variables, i, best_solution
            )

    if best_solution is None:
        print("[ - ] Best solution remains None")
    else:
        print("[ * ] Current best solution:", best_solution)

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


def branch_and_bound(c, A, b, f, minimize, answer_variables, i, best_solution):
    """
    Создает новое ограничение для ветвления и рекурсивно вызывает метод ветвей и границ.
    """
    branching_variable = floor(answer_variables[i])
    A_string = [0 for num in c]
    A_string[i] = 1
    A.append(A_string)
    b.append(branching_variable)

    print(f"[ * ] Adding a new condition for x{i + 1} = {answer_variables[i]}: x{i + 1} <= {b[-1]}; x{i + 1} >= {b[-1] + 1}")
    # print("\n", answer_variables[i], branching_variable, A_string, b)
    # print(c, A, b, f, minimize, "\n")

    best_solution = branches_and_bounds(c, A, b, f, minimize, best_solution)

    b[-1] = (b[-1] + 1) * -1
    A[-1][i] *= -1

    # print("\n[ ? ] more", answer_variables[i], branching_variable, A_string, b)
    # print(c, A, b, f, minimize, "\n")

    best_solution = branches_and_bounds(c, A, b, f, minimize, best_solution)

    return best_solution
