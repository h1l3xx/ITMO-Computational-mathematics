import math


class Result:
    @staticmethod
    def first_function(x: float, y: float):
        return math.sin(x)

    @staticmethod
    def second_function(x: float, y: float):
        return (x * y) / 2

    @staticmethod
    def third_function(x: float, y: float):
        return y - (2 * x) / y

    @staticmethod
    def fourth_function(x: float, y: float):
        return x + y

    @staticmethod
    def default_function(x: float, y: float):
        return 0.0

    # How to use this function:
    # func = Result.get_function(4)
    # func(0.01)
    def get_function(n: int):
        if n == 1:
            return Result.first_function
        elif n == 2:
            return Result.second_function
        elif n == 3:
            return Result.third_function
        elif n == 4:
            return Result.fourth_function
        else:
            return Result.default_function

    def calculate_y_i_next(xi: float, yi, iteration_h, h, func):
        xi_current = xi
        yi_current = yi
        for i in range(iteration_h):
            f_xi_yi = func(xi_current, yi_current)
            delta_yi = h * func(xi_current + h / 2, yi_current + (h / 2) * f_xi_yi)
            yi_current = yi_current + delta_yi
            xi_current += h
        return yi_current

    def solveByEulerImproved(f : int, epsilon, a, y_a, b):
        iteration_h = 10
        h = (b - a) / iteration_h
        function = Result.get_function(f)
        yi_old = Result.calculate_y_i_next(a, y_a, iteration_h, h, function)
        iteration_h += 2
        h = (b - a) / iteration_h
        yi_new = Result.calculate_y_i_next(a, y_a, iteration_h, h, function)

        while abs(yi_new - yi_old) > epsilon:
            yi_old = yi_new
            iteration_h += 2
            h = (b - a) / iteration_h
            yi_new = Result.calculate_y_i_next(a, y_a, iteration_h, h, function)
        return yi_new


if __name__ == '__main__':
    f = int(input().strip())

    epsilon = float(input().strip())

    a = float(input().strip())

    y_a = float(input().strip())

    b = float(input().strip())

    result = Result.solveByEulerImproved(f, epsilon, a, y_a, b)

    print(str(result) + '\n')
