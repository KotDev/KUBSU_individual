import numpy as np
from matplotlib import pyplot as plt

from numerical_methods.lab_3.slau import Slau

class SlauIteration(Slau):
    def __init__(self, matrix: list[list[float]], result: list[float], x_pr: list[float], epsilon: float, w: float = 0.5) -> None:
        super().__init__(matrix=matrix, result=result)
        self.x_pr: list[float] = x_pr
        self.n: int = len(matrix)
        self.epsilon: float = epsilon
        self.w: float = w

    def zeidel(self):
        iterations = 0
        residuals = []
        while True:
            x_next = self.x_pr.copy()
            for i in range(self.n):
                s = sum(self.matrix[i][j] * x_next[j] for j in range(self.n) if j != i)
                x_next[i] = (self.result[i] - s) / self.matrix[i][i]

            residual = np.linalg.norm(
                np.array(self.result) - np.dot(np.array(self.matrix), np.array(x_next))
            )
            residuals.append(residual)

            # Проверка условия остановки
            if all(abs(x_next[i] - self.x_pr[i]) < self.epsilon for i in range(self.n)):
                break

            self.x_pr = x_next
            iterations += 1
        plt.plot(range(len(residuals)), residuals, label="Zeidel")
        plt.xlabel("Iteration")
        plt.ylabel("Residual Norm")
        plt.title("Convergence of Zeidel Method")
        plt.legend()
        plt.grid()
        plt.show()


    def relax_method(self):
        iterations = 0
        residuals = []
        while True:
            x_next = self.x_pr.copy()
            for i in range(self.n):
                s = sum(self.matrix[i][j] * x_next[j] for j in range(self.n) if j != i)
                x_next[i] = self.x_pr[i] + self.w * ((self.result[i] - s) / self.matrix[i][i] - self.x_pr[i])

            residual = np.linalg.norm(
                np.array(self.result) - np.dot(np.array(self.matrix), np.array(x_next))
            )
            residuals.append(residual)

            # Проверка условия остановки
            if all(abs(x_next[i] - self.x_pr[i]) < self.epsilon for i in range(self.n)):
                break

            self.x_pr = x_next
            iterations += 1
        plt.plot(range(len(residuals)), residuals, label="Relaxation")
        plt.xlabel("Iteration")
        plt.ylabel("Residual Norm")
        plt.title("Convergence of Relaxation Method")
        plt.legend()
        plt.grid()
        plt.show()