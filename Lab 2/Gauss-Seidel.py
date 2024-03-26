class Result:
    errorMessage = ""
    isMethodApplicable = True

    @staticmethod
    def solveByGaussSeidel(n, matrix, epsilon):
        indexes = []

        for i in range(n):
            indexes.append(i)

        for i in range(n):
            if len(matrix[i]) != n + 1 or matrix[i][i] == 0:
                Result.error_message = "The system has no diagonal dominance for this method. Method of the " \
                                       "Gauss-Seidel is not applicable."
                Result.isMethodApplicable = False
                return []

        if not check_on_diagonally_dominant(matrix):
            for i in range(len(matrix)):
                if matrix[i][i] > abs_sum_row(matrix[i]) - matrix[i][i]:
                    continue
                elif matrix[i][i] == abs_sum_row(matrix[i]) - matrix[i][i]:
                    continue
                else:
                    for j in range(i + 1, len(matrix)):
                        if matrix[j][i] >= abs_sum_row(matrix[j]) - matrix[j][i]:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            break
            if not check_on_diagonally_dominant(matrix):
                for i in range(len(matrix)):
                    column = []
                    for j in range(len(matrix)):
                        column.append(matrix[j][i])
                    if column[i] > abs_sum(column) - column[i]:
                        continue
                    elif column[i] == abs_sum(column) - column[i]:
                        continue
                    else:
                        for j in range(i + 1, len(matrix)):
                            new_column = []
                            for k in range(len(matrix)):
                                new_column.append(matrix[k][j])
                            if column[i] < abs_sum(column) - column[i]:
                                matrix = change_columns(matrix, i, j)
                                indexes[i], indexes[j] = indexes[j], indexes[i]
                                break
        if not check_on_diagonally_dominant(matrix):
            Result.isMethodApplicable = False
            Result.errorMessage = "The system has no diagonal dominance for this method. Method of the " \
                                  "Gauss-Seidel is not applicable."
            return []

        vector = []
        for i in range(n):
            vector.append(matrix[i][-1])
            matrix[i].pop(-1)

        transform_matrix, transform_vector = transformation(matrix, vector)

        x_n_0 = zero_approximation(transform_vector, vector)

        x_n_1 = [0] * len(transform_matrix)

        x_n_1 = n_approximation(x_n_0, x_n_1, transform_matrix)

        while calc(x_n_0, x_n_1, epsilon):
            x_n_0 = x_n_1
            x_n_1 = [0] * len(transform_matrix)
            x_n_1 = n_approximation(x_n_0, x_n_1, transform_matrix)

        result = []
        for index in indexes:
            result.append(x_n_1[index])
        return result


def abs_sum(line):
    sum = 0
    for i in range(len(line)):
        sum += abs(line[i])
    return sum


def abs_sum_row(row):
    sum = 0
    for i in range(len(row) - 1):
        sum += abs(row[i])
    return sum


def change_columns(matrix, row_1, row_2):
    for i in range(len(matrix)):
        if row_1 != len(matrix) and row_2 != len(matrix):
            matrix[i][row_1], matrix[i][row_2] = matrix[i][row_2], matrix[i][row_1]
    return matrix


def transformation(input_matrix, input_vector):
    buffer = input_vector.copy()
    for i in range(len(input_matrix[0])):
        buffer[i] = input_matrix[i][i]
        input_matrix[i][i] = input_vector[i]
        for j in range(len(input_matrix[i])):
            if input_matrix[i][j] != input_vector[i]:
                input_matrix[i][j] = input_matrix[i][j] * -1
            input_matrix[i][j] = input_matrix[i][j] / buffer[i]
    return input_matrix, buffer


def check_on_diagonally_dominant(matrix):
    diagonally_dominant = False
    counter = 0
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(matrix)):
            if i != j:
                sum += abs(matrix[i][j])
        if abs(matrix[i][i]) > sum:
            diagonally_dominant = True
        if abs(matrix[i][i]) >= sum:
            counter += 1

    if diagonally_dominant and counter == len(matrix):
        return True
    else:
        return False


def zero_approximation(transform_vector, vector):
    return_arr = []
    for i in range(len(vector)):
        return_arr.append(vector[i] / transform_vector[i])
    return return_arr


def n_approximation(x_n_1, x_n_2, transform_matrix):
    return_arr = []
    for i in range(len(transform_matrix)):
        sum = 0
        for j in range(len(transform_matrix)):
            if i == j:
                new_x = transform_matrix[i][j]
            elif j > i:
                new_x = transform_matrix[i][j] * x_n_1[j]
            else:
                new_x = transform_matrix[i][j] * x_n_2[j]
            sum += new_x
        x_n_2[i] = sum
        return_arr.append(sum)
    return return_arr


def calc(x_n_0, x_n_1, epsilon):
    for i in range(len(x_n_0)):
        if x_n_1[i] == 0:
            continue
        calc = (x_n_1[i] - x_n_0[i]) / x_n_1[i]
        if abs(calc) > epsilon:
            return True
    return False


if __name__ == '__main__':
    n = int(input().strip())

    matrix_rows = n
    matrix_columns = n + 1

    matrix = []

    for _ in range(matrix_rows):
        matrix.append(list(map(float, input().rstrip().split())))

    epsilon = float(input().strip())

    result = Result.solveByGaussSeidel(n, matrix, epsilon)
    if Result.isMethodApplicable:
        print('\n'.join(map(str, result)))
    else:
        print(f"{Result.errorMessage}")
