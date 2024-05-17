import math


class ComplexOperation:  # Класс комплексных чисел для операций над ними
    def __init__(self, a: complex, b: complex):  # Инициализируем переменные 2х комплексных чисел
        self.a = a  # Комплексное число а
        self.b = b  # Комплексное число b

    def fold_complex_num(self):  # Операция сложение комплексных чисел
        return self.a + self.b

    def difference_complex_num(self):  # Операция разности комплексных чисел
        return self.a - self.b

    def multiplication_complex_num(self):  # Операция умножения комплексных чисел
        return self.a * self.b

    def division_complex_num(self):  # Операция деления комплексных чисел
        return self.a / self.b


class ComplexForm:  # Класс представления комплексного числа
    def __init__(self, a: complex):  # Инициализируем комплексное число а
        self.a = a  # Комплексное число а

    def degree_complex_num(self, n: int):  # Возведение комплексного числа в целочисленную степень
        return self.a ** n

    def module_complex_num(self):  # Нахождение модуля комплексного числа
        return abs(self.a)

    def arg_complex_num(self):  # Нахождение аргумента комплексного числа
        arg = 0  # Инциализация аргумента комплексного числа
        if self.a.real > 0:  # Если действительная чать < 0
            arg = math.atan(self.a.imag / self.a.real)  # Находим арктангенс y / x
        elif self.a.real < 0 < self.a.imag:  # Если x < 0 < y
            arg = math.atan(self.a.imag / self.a.real) + math.pi  # Находим арктангенс y / x + pi / 2
        elif self.a.real < 0 and self.a.imag < 0:  # Если x < 0 и y < 0
            arg = math.atan(self.a.imag / self.a.real) - math.pi  # Находим арктангенс y / x - pi / 2
        elif self.a.real == 0 and self.a.imag > 0:  # Если x = 0 и y > 0
            arg = math.pi / 2  # Аргумент равен pi / 2
        elif self.a.real == 0 and self.a.imag < 0:  # Если x = 0 и y < 0
            arg = -math.pi / 2  # Аргумент равен -pi / 2
        return arg * math.pi / 180  # аргумент выводится в радианах

    def trig_complex_form(self):  # Представление комплексного числа в триганометрической форме
        arg_complex = self.arg_complex_num()  # Находим аргумент комплексного числа
        module_complex = self.module_complex_num()  # Находим модуль комплексного чиса
        return f"{module_complex} * (cos({round(arg_complex, 3)}) + i * sin({round(arg_complex, 3)}))"

    def expan_complex_form(self):  # Представления комплексного числа в експоненциальной форме
        arg = self.arg_complex_num()  # Находим аргумент комплексного числа
        module_complex = self.module_complex_num()  # Находим модуль комплексного числа
        return f"{module_complex} * e^(i * {round(arg, 3)})"


class ComplexFormTranslation(ComplexForm):  # Класс представления комплексного числа из одной формы в другую
    def __init__(self, arg: int, module: float):  # Инициализируем аргумент и модуль комплексного числа
        self.arg = arg  # Переменная аргумента комплексного числа
        self.module = module  # Переменная модели комплексного числа

    def trig_algebra_complex_form(self):  # Перевод из триганометрической формы в алгебраическую форму
        real_num = round(math.cos(self.arg * math.pi / 180) * self.module, 2)  # Находим действительную часть
        img_num = round(math.sin(self.arg * math.pi / 180) * self.module, 2)  # Находим действительную часть
        return complex(real=real_num, imag=img_num)

    def trig_expan_complex_form(self):  # Перевод из триганометрической в экспоненциальную форму
        return f"{self.module} * e^(i * {round(self.arg * math.pi / 180, 3)})"

    def expan_algebra_complex_form(self):  # Перевод из экспоненциальной в алгебраическую форму
        complex_num = self.module * math.e ** (1j * (self.arg * math.pi / 180))  # находим комплексное число
        real_num = round(complex_num.real, 2)  # Округляем действительную часть до 2х знаков после запятой
        img_num = round(complex_num.imag, 2)  # Округляем мнимую часть до 2х знаков после запятной
        return complex(real=real_num, imag=img_num)

    def expan_trig_complex_form(self):  # Перевод из экспоненциальной формы в триганометрическую форму
        return f"{self.module} * (cos({round(self.arg * math.pi / 180, 3)}) + i * sin({round(self.arg * math.pi / 180, 3)}))"