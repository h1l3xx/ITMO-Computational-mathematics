

import math



def first_function(args: []) -> float:
    return math.sin(args[0])


def second_function(args: []) -> float:
    return (args[0] * args[1]) / 2


def third_function(args: []) -> float:
    return (pow(args[0], 2) * pow(args[1], 2)) - (3 * pow(args[0], 3)) - (6 * pow(args[1], 3)) + 8


def fourth_function(args: []) -> float:
    return pow(args[0], 4) - 9 * args[1] + 2


def fifth_function(args: []) -> float:
    return args[0] + pow(args[0], 2) - 2 * args[1] * args[2] - 0.1


def six_function(args: []) -> float:
    return args[1] + pow(args[1], 2) + 3 * args[0] * args[2] + 0.2


def seven_function(args: []) -> float:
    return args[2] + pow(args[2], 2) + 2 * args[0] * args[1] - 0.3


def default_function(args: []) -> float:
    return 0.0


# How to use this function:
# funcs = Result.get_functions(4)
# funcs[0](0.01)
def get_functions(n: int):
    if n == 1:
        return [first_function, second_function]
    elif n == 2:
        return [third_function, fourth_function]
    elif n == 3:
        return [fifth_function, six_function, seven_function]
    else:
        return [default_function]


#
# Complete the 'solve_by_fixed_point_iterations' function below.
#
# The function is expected to return a DOUBLE_ARRAY.
# The function accepts following parameters:
#  1. INTEGER system_id
#  2. INTEGER number_of_unknowns
#  3. DOUBLE_ARRAY initial_approximations
#

def solve_by_fixed_point_iterations(system_id, n, initial_approximations):
    current_func = get_functions(system_id)
    current_approximations = initial_approximations.copy()
    new_approximations = [0.0] * n
    result_qualifier = [0.0001] * n
    epsilon = 0.0000001

    iterations = 100000

    while iterations > 0:
        for i in range(n):
            try:
                new_approximations[i] = current_approximations[i] - current_func[i](current_approximations) * result_qualifier[i]
            except Exception as e:
                raise ArithmeticError(
                    "The method is not applicable due to the initial conditions"
                )
        is_end = True
        for i in range(n):
            if abs(current_approximations[i] - new_approximations[i]) < epsilon:
                continue
            else:
                is_end = False
                break
        if is_end:
            return new_approximations

        for i in range(n):

            value_current_approximations = abs(current_func[i](current_approximations))
            value_new_approximations = abs(current_func[i](new_approximations))

            if value_current_approximations < value_new_approximations:
                result_qualifier[i] = -result_qualifier[i]
        current_approximations = new_approximations.copy()
    raise IndexError(
        "Too many iterations"
    )


if __name__ == '__main__':
    system_id = int(input().strip())

    number_of_unknowns = int(input().strip())

    initial_approximations = []

    for _ in range(number_of_unknowns):
        initial_approximations_item = float(input().strip())
        initial_approximations.append(initial_approximations_item)

    result = solve_by_fixed_point_iterations(system_id, number_of_unknowns, initial_approximations)

    print('\n'.join(map(str, result)))
