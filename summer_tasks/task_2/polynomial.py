import sympy
# библиотека несёт исключительно визуал и никак не влияет на вычисления полинома


arr_x = list()
arr_y = list()


def w(x: int, index: int) -> tuple:
    """
    Функция w вычисляет фундаментальные многочлены w1, w2 ... wn

    param x: int
    param index: int
    return: tuple

    """
    res_1 = 1  # результат для числителя
    res_2 = 1  # результат для знаменателя
    view_x = sympy.Symbol("x")  # задаём символ х как мат.элемент для представления полинома
    view_w = 1  # все степени полинома будут находится в числителе
    for i in range(len(arr_x)):
        if index != i:  # проверяем что бы w != индексу x для предотвращения 0 в знаменателе
            res_1 *= x - arr_x[i]  # находим числитель (x - x1)(x - x2) ... (x - xn-1)
            view_w *= view_x - arr_x[i]  # находим произведение (x - x1) (x - x2)... для представления полинома
            res_2 *= arr_x[index] - arr_x[i]  # находим знаменатель (xi - x2) (xi - x3) ... где i зависит от wi
    return res_1 / res_2, view_w / res_2


def F(x: int) -> tuple:
    """
    F(x) вычисляет интерполяцию и строит интерполяционный полином Лагранжа:
    F(x) = y1 * w1 + y2 * x2 + ... yn * wn

    param x: int
    return: tuple

    """
    res_f = 0  # результат интреполяции
    polinom_view = 0  # полином
    for i in range(len(arr_x)):
        w_i = w(x, i)  # находим wi
        y = arr_y[i]  # присваеваем соответсвующий y т.е f: x->y
        res_f += y * w_i[0]  # умножаем y на значения wi
        polinom_view += y * w_i[1]  # умножаем y на наш получившийся полином wi для представления полинома
    res_p = polinom_view.as_poly()  # строим сам полином
    res_v = res_p.as_expr()  # вывод полинома
    return res_f, res_v
