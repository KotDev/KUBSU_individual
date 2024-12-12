from math import sin

from matplotlib import pyplot as plt
from pydantic.fields import Callable
from scipy.integrate import solve_ivp


class DifurMethods:
    def __init__(self, f: Callable, x0: int, y0: int, x_end: int, h_values: list[float]):
        self.f = f
        self.x0 =x0
        self.y0 = y0
        self.x_end = x_end
        self.h_values = h_values

    def exact_solution(self, x):
        if x == 0:
            return self.y0  # Если x = 0, возвращаем начальное значение

            # Попробуем найти решение
        try:
            sol = solve_ivp(self.f, [self.x0, x], [self.y0], t_eval=[x])  # Решаем задачу Коши
            if sol.success and len(sol.y) > 0:  # Решение существует
                return sol.y[0][0]  # Вернем значение в точке x
            else:
                print(f"Не удалось найти решение для x={x}")
                return None
        except Exception as e:
            print(f"Ошибка при вычислении точного решения: {e}")
            return None


    def euler_method(self, h, n):
        x_values = [self.x0]
        y_values = [self.y0]
        for i in range(n):
            y_next = y_values[-1] + h * self.f(x_values[-1], y_values[-1])
            x_next = x_values[-1] + h
            x_values.append(x_next)
            y_values.append(y_next)
        return x_values, y_values

    def runge_kutta_2nd_order(self, h, n):
        x_values = [self.x0]
        y_values = [self.y0]
        for i in range(n):
            k1 = self.f(x_values[-1], y_values[-1])
            k2 = self.f(x_values[-1] + h / 2, y_values[-1] + h / 2 * k1)
            y_next = y_values[-1] + h * k2
            x_next = x_values[-1] + h
            x_values.append(x_next)
            y_values.append(y_next)
        return x_values, y_values

    def solve_and_plot(self):
        plt.figure(figsize=(12, 8))

        # Точное решение
        x_exact = [self.x0 + i * 0.01 for i in range(int((self.x_end - self.x0) / 0.01) + 1)]
        y_exact = [self.exact_solution(x) for x in x_exact]
        plt.plot(x_exact, y_exact, label="Точное решение", color="black", linewidth=2)

        for h in self.h_values:
            n = int((self.x_end - self.x0) / h)

            # Метод Эйлера
            x_euler, y_euler = self.euler_method(h, n)
            plt.plot(x_euler, y_euler, linestyle='--', marker='o', label=f"Эйлер, шаг={h}")

            # Метод Рунге-Кутта 2-го порядка
            x_rk2, y_rk2 = self.runge_kutta_2nd_order(h, n)
            plt.plot(x_rk2, y_rk2, linestyle='-', marker='x', label=f"Рунге-Кутта 2-го, шаг={h}")

        # Оформление графика
        plt.title("Решение задачи Коши методами Эйлера и Рунге-Кутта")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show()



def f(x, y):
    return x**2 + y
x0 = 0
y0 = 1
x_end = 1
h_values = [0.1, 0.05, 0.01]
method = DifurMethods(f, x0, y0, x_end, h_values)
method.solve_and_plot()