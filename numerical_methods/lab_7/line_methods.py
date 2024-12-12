# Метод деления отрезка пополам
def bisection_method(f, a, b, tol):
    if f(a) * f(b) >= 0:
        print("Метод деления отрезка пополам не может быть применен.")
        return None

    while (b - a) / 2 > tol:
        c = (a + b) / 2
        if f(c) == 0:  # нашли точный корень
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2

# Метод секущих
def secant_method(f, x0, x1, tol, max_iter=100):
    for _ in range(max_iter):
        if abs(f(x1)) < tol:
            return x1
        try:
            x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        except ZeroDivisionError:
            print("Деление на ноль при вычислении.")
            return None
        x0, x1 = x1, x2
    print("Метод секущих не сошелся за указанное число итераций.")
    return None

# Пример использования
if __name__ == "__main__":
    # Функция F(x) = x^2 - 2
    def f(x):
        return x**2 - 2

    # Интервал для метода деления пополам
    a, b = 1, 2
    tol = 1e-5

    print("Метод деления отрезка пополам:")
    root_bisection = bisection_method(f, a, b, tol)
    print(f"Найденный корень: {root_bisection}")

    # Начальные приближения для метода секущих
    x0, x1 = 1, 2

    print("\nМетод секущих:")
    root_secant = secant_method(f, x0, x1, tol)
    print(f"Найденный корень: {root_secant}")
