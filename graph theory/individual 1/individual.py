def algorithm_hackimi(vertices: list) -> bool:

    """
    Функция для нахождения простого графа по алгоритму Хавел-Хакими

    Параметры функции:
    :param vertices:
    :return:
    """

    if any([i < 0 for i in vertices]):  # Проверяем список на 0 элементы т.е [0, 0, 0, 0]
        return False

    if all([i == 0 for i in vertices]):  # Проверяем списко на хотя бы 1 отрицательный элемент т.е [0, -1, -1, 0]
        return True

    vertices.sort()  # Сортируем список степеней вершин по возрастанию

    last = vertices[-1]  # Берем последний элемент т.к он максимальный в списке
    vertices.remove(last)  # Удаляем этот самый максимальны элемент

    # Проходимся по остальным элементам списка от конца к началу
    for i in range(len(vertices) - 1, len(vertices) - last - 1, -1):
        if vertices[i] > 0:  # Проверяем элемент на отрицательность
            vertices[i] -= 1  # Отнимаем от него 1
        else:  # Если элемент отрицательный то получаем не рекурентную ветку
            return False

    # Возвращаем функцию для рекурсии
    return algorithm_hackimi(vertices)


def examination_vertices(vertices: list) -> bool:

    """
    Функция на проверку теорем о существовании
    1. Во всяком графе с n вершинами (n >2) всегда найдутся, по меньшей мере, две вершины с одинаковыми степенями
    2. Если в графе с n вершинами (n >2) в точности две вершины имеют одинаковую степень, то в этом графе всегда
    найдется либо в точности одна вершина степени 0, либо в точности одна вершина степени n - 1.

    Параметры функции
    :param vertices:
    :return:
    """

    # Создаём хэш таблицу (словарь) для хранения кол-во повторяющихся степеней
    count_vertices_dict = {i: vertices.count(i) for i in set(vertices)}

    # Сортируем хэш таблицу (словарь) по убыванию
    count_vertices_dict = dict(reversed(sorted(count_vertices_dict.items())))

    # Проверяем на то что существет хотя бы 1 степень вершины которая повторяется 2 и более раз
    if any([i >= 2 for i in count_vertices_dict.values()]):
        for k, v in count_vertices_dict.items():  # Проходимся по степеням вершин
            #  Если этой вершины 2 и более то должна сущ такая вершина v-1 или 0 в списке вершин
            if v >= 2 and not (k-1 in count_vertices_dict or 0 in count_vertices_dict):
                return False
            elif v >= 2:
                return True
    else:
        return False
    return True


def main_individual() -> str:

    """
    Главная функция для проверки на существования и выявлении типа графа
    :return:
    """

    count_vertices = int(input("Введите кол-во вершин: "))  # Вводим кол-во вершин

    # Вводим сами степени вершин
    vertices_degree = [int(input(f"Введите вершину: {i + 1} - ")) for i in range(count_vertices)]
    if any([i < 0 for i in vertices_degree]):  # Проверяем степени на отрицание
        return "В графе все степени вершин должны быть положительными"
    sort_vertices = [i for i in vertices_degree if i != 0]  # Удаляем нулевые вершины графа
    if not sort_vertices:  # Проверяем не состоит ли граф только из нулевых вершин
        return "Граф не связанный"

    # Проверяем на чётность кол-во нечёт элементов
    bool_count_odd_vertices = len([i for i in sort_vertices if i % 2 != 0]) % 2 == 0
    sum_vertices = sum(sort_vertices)  # Вычисляем сумму степенней вершин

    # Проверяем существования мульти графа
    multi_graph = count_vertices < sum_vertices and sum_vertices % 2 == 0 and bool_count_odd_vertices

    # Проверяем существования полного графа
    full_graph = ((count_vertices * (count_vertices - 1)) / 2) * 2 == sum_vertices
    if len(vertices_degree) > 2:  # При степени кол-во степеней вершин > 2 добовляем условие к существованию графа
        full_graph = full_graph and examination_vertices(vertices_degree)
        multi_graph = multi_graph and examination_vertices(vertices_degree)

    # Проверяем существования простого графа
    simple_graph = (count_vertices < sum_vertices and sum_vertices % 2 == 0 and examination_vertices(vertices_degree)
                    and algorithm_hackimi(vertices_degree))

    if full_graph:
        return "Граф полный"
    elif simple_graph:
        return "Простой граф"
    elif multi_graph:
        return "Мультиграф"
    else:
        return "Такой граф построить нельзя"


if "__main__" == __name__:
    print(main_individual())

