def internal_stability_num(list_vertex: list, len_vertex: int) -> int:
    """ Функция нахождения числа внутренней устойчивости графа
        param: list_vertex: list
        param: len_vertex: int
        return: int
    """
    vertex_2 = []  # создаём список для конъюнкции 2х скобок
    set_vertex = []  # создаём список который будет хранить все элементы ДНФ с учётом операции поглощения
    index = 0  # индекс для list_vertex
    while len(list_vertex) > 1:  # пока не сделаем конъюнкцию всех скобок
        for i in list_vertex[index]:  # проходим по связям (xi, xj)
            for j in list_vertex[index + 1]:  # проходим по связям (xi + 1, xj + 1)
                vertex_2.append(i + " " + j)  # записываем перемножение скобок (xi, xj) (xi + 1, xj + 1)
        list_vertex.pop(index)  # удаляем (xi, xj) из list_vertex
        list_vertex.pop(index)  # удаляем (xi + 1, xj + 1) из list_vertex
        list_vertex.insert(index, vertex_2)   # добавляем перемноженную скобку в list_vertex
        vertex_2 = []  # очищаем список в котором перемножали скобки
    list_vertex = list_vertex[0]

    for elem in list_vertex:  # проходимся по ДНФ и выполняем закон поглощения
        if set(elem.split()) not in set_vertex:  # проверяем что такого элемента нет в списке
            set_vertex.append(set(elem.split()))  # добавляем в список элемент
    # находим дизъюнкт состоящий из минимальных элементов, разность кол-во всех вершин и минимального дизъюнкта
    return len_vertex - len(min(set_vertex, key=lambda x: len(x)))
