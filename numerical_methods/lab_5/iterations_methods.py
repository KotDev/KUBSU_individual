from math import atan, cos, sin


class Iterations:
    def __init__(self, matrix: list[list[float]], epsilon: float):
        self.matrix = matrix
        self.epsilon = epsilon
        self.max_iter = 1000

    def matrix_mult_vector(self, vector: list[float]):
        """Умножение матрицы на вектор."""
        return [sum(self.matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(self.matrix))]

    @staticmethod
    def normal_vector(vector: list[float]):
        """Евклидова норма вектора."""
        return sum(x ** 2 for x in vector) ** 0.5

    @staticmethod
    def scalar_vectors(vector_1: list[float], vector_2: list[float]):
        """Скалярное произведение двух векторов."""
        return sum(x * y for x, y in zip(vector_1, vector_2))

    def power_iteration_method(self):
        """Метод прямой итерации для поиска наибольшего собственного числа."""
        n = len(self.matrix)
        b = [1.0] * n
        b = [x / self.normal_vector(b) for x in b]

        eigenvalue_old = 0
        for iteration in range(self.max_iter):
            b_new = self.matrix_mult_vector(b)
            b_new_norm = self.normal_vector(b_new)
            b_new = [x / b_new_norm for x in b_new]
            eigenvalue = self.scalar_vectors(b_new, self.matrix_mult_vector(b_new))
            if abs(eigenvalue - eigenvalue_old) < self.epsilon:
                return eigenvalue, b_new, iteration + 1
            eigenvalue_old = eigenvalue
            b = b_new
        raise ValueError("Метод не сошелся за заданное число итераций")

    def max_offdiag_element(self):
        """Поиск наибольшего внедиагонального элемента."""
        n = len(self.matrix)
        max_val = 0
        p, q = 0, 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(self.matrix[i][j]) > max_val:
                    max_val = abs(self.matrix[i][j])
                    p, q = i, j
        return p, q, max_val

    def rotate(self, p, q):
        """Выполняет вращение матрицы для элементов p, q."""
        if self.matrix[p][p] == self.matrix[q][q]:
            theta = 3.141592653589793 / 4  # pi/4
        else:
            theta = 0.5 * atan(2 * self.matrix[p][q] / (self.matrix[p][p] - self.matrix[q][q]))

        cos_t = cos(theta)
        sin_t = sin(theta)

        n = len(self.matrix)
        R = [[self.matrix[i][j] for j in range(n)] for i in range(n)]

        for i in range(n):
            if i != p and i != q:
                R[i][p] = cos_t * self.matrix[i][p] - sin_t * self.matrix[i][q]
                R[p][i] = R[i][p]
                R[i][q] = sin_t * self.matrix[i][p] + cos_t * self.matrix[i][q]
                R[q][i] = R[i][q]

        R[p][p] = cos_t ** 2 * self.matrix[p][p] + 2 * cos_t * sin_t * self.matrix[p][q] + sin_t ** 2 * self.matrix[q][
            q]
        R[q][q] = sin_t ** 2 * self.matrix[p][p] - 2 * cos_t * sin_t * self.matrix[p][q] + cos_t ** 2 * self.matrix[q][
            q]
        R[p][q] = R[q][p] = 0

        return R, cos_t, sin_t

    def jakobi_method(self):
        """Метод Якоби для поиска всех собственных чисел."""
        n = len(self.matrix)
        V = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

        for iteration in range(self.max_iter):
            p, q, max_offdiag = self.max_offdiag_element()
            if max_offdiag < self.epsilon:
                eigenvalues = [self.matrix[i][i] for i in range(n)]
                return eigenvalues, V, iteration

            self.matrix, cos_t, sin_t = self.rotate(p, q)

            # Обновляем матрицу собственных векторов
            for i in range(n):
                V_i_p = V[i][p]
                V_i_q = V[i][q]
                V[i][p] = cos_t * V_i_p - sin_t * V_i_q
                V[i][q] = sin_t * V_i_p + cos_t * V_i_q

        raise ValueError("Метод не сошелся за заданное число итераций")


# Пример использования
A = [[4, 1],
     [1, 3]]
