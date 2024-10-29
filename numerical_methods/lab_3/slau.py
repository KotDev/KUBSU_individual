

class Slau:
    def __init__(self, matrix: list[list[float]], result: list[float]) -> None:
        self.matrix: list[list[float]] = matrix
        self.result: list[float] = result


    def method_gaus(self):
        eps: float = 0.0001
        len_matrix: int = 0
        while len_matrix < len(self.matrix):
            max_elem: int = 0
            index: int = len_matrix
            for i in range(len_matrix, len(self.matrix)):
                if abs(self.matrix[i][len_matrix]) > max_elem:
                    max_elem = abs(self.matrix[i][len_matrix])
                    index = i
            if max_elem < eps:
                print("В матрице есть нулевой столбец")
                return
            if index != len_matrix:
                self.matrix[len_matrix], self.matrix[index] = self.matrix[index], self.matrix[len_matrix]
                self.result[len_matrix], self.result[index] = self.result[index], self.result[len_matrix]
            lead_elem = self.matrix[len_matrix][len_matrix]
            for j in range(len(self.matrix[0])):
                self.matrix[len_matrix][j] /= lead_elem
            self.result[len_matrix] /= lead_elem
            for i in range(len_matrix + 1, len(self.matrix)):
                factor = self.matrix[i][len_matrix]
                for j in range(len(self.matrix[0])):
                    self.matrix[i][j] -= factor * self.matrix[len_matrix][j]
                self.result[i] -= factor * self.result[len_matrix]

            len_matrix += 1
        result: list[float] = [0 for _ in range(len(self.result))]
        for i in range(len(self.result) - 1, -1, -1):  # Идем с конца к началу
            result[i] = self.result[i]
            for j in range(i + 1, len(self.result)):
                result[i] -= self.matrix[i][j] * result[j]
        self.result = result

    def method_running(self):
        y = self.matrix[0][0]
        alpha = -self.matrix[0][1] / y
        betta = self.result[0] / y
        betta_list = [betta]
        alpha_list = [alpha]
        for i in range(1, len(self.matrix)):
            y_i = self.matrix[i][i] + self.matrix[i][i-1] * alpha_list[i - 1]
            if i != len(self.matrix) - 1:
                alpha_i = -self.matrix[i][i+1] / y_i
                alpha_list.append(alpha_i)
            betta_i = (self.result[i] - self.matrix[i][i-1] * betta_list[i - 1]) / y_i
            betta_list.append(betta_i)

        self.result[-1] = betta_list[-1]
        for i in range(len(self.result) - 2, -1, -1):
            self.result[i] = alpha_list[i] * self.result[i + 1] + betta_list[i]



slau = Slau(matrix=[
            [2, -1, 0],
            [5, 4, 2],
            [0, 1, -3]
                    ],
            result=[3, 6, 2]
            )

