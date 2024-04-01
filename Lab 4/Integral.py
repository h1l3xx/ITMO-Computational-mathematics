import math


class Result:
    error_message = ""
    has_discontinuity = False
    eps = 0

    @staticmethod
    def first_function(x: float):
        return 1 / x

    @staticmethod
    def second_function(x: float):
        if x == 0:
            return (math.sin(Result.eps) / Result.eps + math.sin(-Result.eps) / -Result.eps) / 2
        return math.sin(x) / x

    @staticmethod
    def third_function(x: float):
        return x * x + 2

    @staticmethod
    def fourth_function(x: float):
        return 2 * x + 2

    @staticmethod
    def five_function(x: float):
        return math.log(x)

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
        elif n == 5:
            return Result.five_function
        else:
            raise NotImplementedError(f"Function {n} not defined.")

    def calculate_approximation(a: float, b: float, h, func):
        first_and_last_elements_sum = 0
        sum_elements_even_index = 0
        sum_elements_odd_index = 0

        values = [a]
        loop_value = a

        while loop_value < b:
            loop_value += h
            values.append(loop_value)
        for i in range(len(values)):
            try:
                func(values[i])
            except ZeroDivisionError or ValueError as e:
                if e != ValueError:
                    if abs(a) == abs(b):
                        return 0
                    else:
                        return "error"
                return "error"
            if i == 0 or i == len(values) - 1:
                first_and_last_elements_sum += func(values[i])
            elif i % 2 == 0:
                sum_elements_even_index += func(values[i])
            else:
                sum_elements_odd_index += func(values[i])
        return (h / 3) * (first_and_last_elements_sum + 2 * sum_elements_even_index + 4 * sum_elements_odd_index)

    def calculate_integral(a: float, b: float, f, epsilon):

        Result.eps = epsilon
        current_function = Result.get_function(f)
        if b < a:
            inner_b = a
            inner_a = b
        else:
            inner_b = b
            inner_a = a
        h = (inner_b - inner_a) / 2
        n = 2
        old_value = Result.calculate_approximation(inner_a, inner_b, h, current_function)
        if old_value == 0:
            return 0
        elif old_value == "error":
            Result.error_message = "Integrated function has discontinuity or does not defined in current interval"
            Result.has_discontinuity = True
            return 0
        while True:
            new_h = (inner_b - inner_a) / (2 * n)
            new_value = Result.calculate_approximation(inner_a, inner_b, new_h, current_function)
            if new_value == 0:
                return 0
            elif new_value == "error":
                Result.error_message = "Integrated function has discontinuity or does not defined in current interval"
                Result.has_discontinuity = True
                return 0
            if abs(old_value - new_value) < Result.eps:
                if b < a:
                    return new_value * (-1)
                else:
                    return new_value
            n += 1
            old_value = new_value

    #
    # Complete the 'calculate_integral' function below.
    #
    # The function is expected to return a DOUBLE.
    # The function accepts following parameters:
    #  1. DOUBLE a
    #  2. DOUBLE b
    #  3. INTEGER f
    #  4. DOUBLE epsilon
    #


# Write your code here


if __name__ == '__main__':

    a = float(input().strip())

    b = float(input().strip())

    f = int(input().strip())

    epsilon = float(input().strip())

    result = Result.calculate_integral(a, b, f, epsilon)
    if not Result.has_discontinuity:
        print(str(result) + '\n')
    else:
        print(Result.error_message + '\n')
