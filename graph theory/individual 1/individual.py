import networkx as nx
import matplotlib.pyplot as plt


def algorithm_hackimi(vertices: list, result: list) -> bool:

    """
    Функция для нахождения простого графа по алгоритму Хавел-Хакими

    Параметры функции:
    :param vertices:
    :param result
    :return:
    """

    if any([i[1] < 0 for i in vertices]):  # Проверяем список на 0 элементы т.е [0, 0, 0, 0]
        return False

    if all([i[1] == 0 for i in vertices]):  # Проверяем списка на хотя бы 1 отрицательный элемент т.е [0, -1, -1, 0]
        return True

    vertices.sort(key=lambda x: x[1])  # Сортируем список степеней вершин по возрастанию

    last = vertices[-1]  # Берем последний элемент т.к он максимальный в списке
    vertices.remove(last)  # Удаляем этот самый максимальны элемент

    # Проходимся по остальным элементам списка от конца к началу
    for i in range(len(vertices) - 1, len(vertices) - last[1] - 1, -1):
        if vertices[i][1] > 0:  # Проверяем элемент на отрицательность
            vertices[i][1] -= 1  # Отнимаем от него 1
            val = (last[0], vertices[i][0])  # Формируем связь
            result.append(val)  # Добавляем связь в список
        else:  # Если элемент отрицательный, то получаем не рекурентную ветку
            return False

    # Возвращаем функцию для рекурсии
    return algorithm_hackimi(vertices, result)


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
    # Именуем каждую вершину графа, 0 вершины не учитываются
    dict_vertices = [list(j) for j in list({i: sort_vertices[i] for i in range(len(sort_vertices))}.items())]
    result_vertices = list()  # Список связей вершин графа
    if not sort_vertices:  # Проверяем не состоит ли граф только из нулевых вершин
        return "Граф не связанный"

    sum_vertices = sum(sort_vertices)  # Вычисляем сумму степенней вершин
    vertices_graph = algorithm_hackimi(dict_vertices, result_vertices)  # Строим граф по алгоритму Хавел-Хакими
    # Проверяем существования полного графа
    full_graph = ((count_vertices * (count_vertices - 1)) / 2) * 2 == sum_vertices
    # Проверяем существования простого графа
    simple_graph = (count_vertices <= sum_vertices and sum_vertices % 2 == 0 and vertices_graph)
    # Проверяем существование графа и рисуем его
    if (full_graph or simple_graph):
        G = nx.Graph()  # Создаем класс графа
        G.add_edges_from(result_vertices)  # Добавляем к нему связанные вершины
        nx.draw(G, with_labels=True, font_weight='bold')  # Рисуем граф
        plt.show()  # Выводим граф на экран
    if full_graph:
        return "Граф полный"
    elif simple_graph:
        return "Простой граф"
    else:
        return "Такой граф построить нельзя"


if "__main__" == __name__:
    print(main_individual())

