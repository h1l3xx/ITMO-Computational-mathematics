import math


class FunctionSet:

    def weierstrass_function(x: float):
        f_x = 0
        n = 5
        b = 0.5
        a = 13
        for i in range(n):
            f_x += pow(b, i) * math.cos(pow(a, n) * math.pi * x)

        return f_x

    def gamma_function(x: float):
        # made for consistency with other languages. Normally math.gamma can be used.
        tmp = (x - 0.5) * math.log(x + 4.5) - (x + 4.5)
        ser = 1.0 + 76.18009173 / (x + 0.0) - 86.50532033 / (x + 1.0) + 24.01409822 / (x + 2.0) - 1.231739516 / (
                x + 3.0) + 0.00120858003 / (x + 4.0) - 0.00000536382 / (x + 5.0)

        return math.exp(tmp + math.log(ser * math.sqrt(2 * math.pi)))
    def parabola(x: float):
        return x*x
    # How to use this function:
    # func = FunctionSet.get_function(4)
    # func(0.01)
    def get_function(n: int):
        if n == 1:
            return FunctionSet.weierstrass_function
        elif n == 2:
            return FunctionSet.gamma_function
        elif n == 3:
            return FunctionSet.parabola
        else:
            raise NotImplementedError(f"Function {n} not defined.")


def get_array_with_chebyshev_roots_and_values(a, b, n, func):
    array = []
    for i in range(0, n):
        chebyshev_root = ((a + b) / 2 + ((b - a) / 2) * math.cos((math.pi * (2 * i + 1)) / (2 * n + 2)))
        array.append([chebyshev_root, func(chebyshev_root)])
    return array


def interpolate_by_newton(function_number, left_border_value, right_border_value, value):
    start_first_array = get_array_with_chebyshev_roots_and_values(
        left_border_value,
        right_border_value,
        1,
        FunctionSet.get_function(function_number)
    )
    start_second_array = get_array_with_chebyshev_roots_and_values(
        left_border_value,
        right_border_value,
        2,
        FunctionSet.get_function(function_number)
    )
    iterator = 3
    old = interpolate(start_first_array, value)
    new = interpolate(start_second_array, value)
    while abs(new - old) >= 0.01:
        old = new
        new = interpolate(
            get_array_with_chebyshev_roots_and_values(
                left_border_value,
                right_border_value,
                iterator,
                FunctionSet.get_function(function_number)
            ),
            value
        )
        iterator = iterator + 1
    return new


def interpolate(data, x_value):
    x_data = []
    y_data = []
    for i in range(0, len(data)):
        x_data.append(data[i][0])
        y_data.append(data[i][1])

    coefficients = get_coefficients(x_data, y_data)
    n = len(x_data) - 1
    count_value = coefficients[n]

    for k in range(1, n + 1):
        count_value = coefficients[n - k] + (x_value - x_data[n - k])*count_value

    return count_value


def get_coefficients(x_array, y_array):
    n = len(x_array)

    coefficients = y_array.copy()
    x_data = x_array.copy()
    for k in range(1, n):
        slice_coefficients = coefficients[k:n].copy()
        slice_x_data = x_data[k:n].copy()
        first_clause = []
        second_clause = []
        for number in slice_coefficients:
            first_clause.append(number - coefficients[k - 1])
        for number in slice_x_data:
            second_clause.append(number - x_data[k - 1])
        for i in range(len(first_clause)):
            first_clause[i] = second_clause[i] and first_clause[i] / second_clause[i]
        coefficients[k:n] = first_clause

    return coefficients


f = int(input())
a = float(input())
b = float(input())
x = float(input())

print(interpolate_by_newton(f, a, b, x))
