import matplotlib.pyplot as plt
import numpy as np


class MethodsIntegrals:
    def __init__(self, function):
        self.function = function

    def __left_integral_calculation(self, a: float, b: float, step: int) -> float:
        delta_x = (a - b) / step
        integral_sum: float = 0
        for i in range(step):
            integral_sum += self.function(a + i * delta_x) * delta_x
        return integral_sum


    def __right_integral_calculation(self, a: float, b: float, step: int) -> float:
        delta_x = (a - b) / step
        integral_sum: float = 0
        for i in range(1, step + 1):
            integral_sum += self.function(a + i * delta_x) * delta_x
        return integral_sum


    def __mid_integral_calculation(self, a: float, b: float, step: int) -> float:
        delta_x = (a - b) / step
        integral_sum: float = 0
        for i in range(step):
            integral_sum += self.function(a + (i + 0.5) * delta_x) * delta_x
        return integral_sum


    def __runge_rule_method(self, a: float, b: float, step: int, method: str) -> float:
        double_step: int = step * 2
        match method:
            case "left":
                integral= self.__left_integral_calculation(a, b, step)
                double_integral = self.__left_integral_calculation(a, b, double_step)
            case "right":
                integral = self.__right_integral_calculation(a, b, step)
                double_integral = self.__right_integral_calculation(a, b, double_step)
            case "mid":
                integral = self.__mid_integral_calculation(a, b, step)
                double_integral = self.__mid_integral_calculation(a, b, double_step)
            case _:
                integral = 0
                double_integral = 0
        return abs(double_integral - integral) / 3


    def integrate(self, a: float, b: float, accuracy: float, method: str):
        step: int = 1
        while True:
            range_rule = self.__runge_rule_method(a, b, step, method)
            if range_rule <= accuracy:
                break
            step *= 2
            match method:
                case "left":
                    integral = self.__left_integral_calculation(a, b, step)
                case "right":
                    integral = self.__right_integral_calculation(a, b, step)
                case "mid":
                    integral = self.__mid_integral_calculation(a, b, step)
                case _:
                    integral = 0
                    break
        return integral, step,  (a - b) / step


class Schedule(MethodsIntegrals):
    def __init__(self, function, a, b, accuracy, method):
        super().__init__(function)
        self.method = method
        self.integral, self.n, self.step = self.integrate(a, b, accuracy, self.method)
        self.x = np.linspace(a, b, self.n + 1)
        self.y = self.function(self.x)

    def render(self):
        start: int = 0
        if self.method == "right":
            self.n += 1
            start = 1
        for i in range(start, self.n):
            plt.bar(self.x[i],
                    self.y[i],
                    width=self.step,
                    align="edge",
                    alpha=0.5,
                    edgecolor="black",
                    label=self.method + " rectangle" if i == 0 else None
                    )
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.show()



