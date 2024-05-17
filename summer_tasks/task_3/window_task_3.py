import wx
from wx.grid import Grid
from DNF_and_num_stability import internal_stability_num
import matplotlib.pyplot as plt
import networkx as nx


class WindowApp(wx.Frame):  # описываем базовый класс нашего окна
    def __init__(self, *args, **kw):
        """Инициализируем все виджеты и панель, получаем все методы и атрибуты унаследованного"""
        super(WindowApp, self).__init__(*args, **kw, size=(900, 400))

        self.panel = wx.Panel(self)  # создаём панель окна
        self.grid = Grid(self.panel)  # создаём таблицу
        self.G = nx.Graph()  # создаём заранее объект графа

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.color_value_table)

        # создаём кнопку "принять" и input виджет
        self.size_table_button = wx.Button(self.panel, label="Принять", size=(100, 30))  # создаём виджет кнопки
        self.size_table_button.Bind(wx.EVT_BUTTON, self.create_table)  # привязываем кнопку к функции
        # создаём input виджет
        self.input_size = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=(300, -1))
        self.input_size.SetHint("Размерность таблицы n x n")

        # создаём кнопку назад
        self.back_button = wx.Button(self.panel, label="Назад", size=(100, 30))  # создаём виджет кнопки
        self.back_button.Bind(wx.EVT_BUTTON, self.back_window)  # привязываем кнопку к функции

        # создаём кнопку отрисовки графа
        self.graph_button = wx.Button(self.panel, label='граф', size=(100, 30))  # создаём виджет кнопки
        self.graph_button.Bind(wx.EVT_BUTTON, self.graph_paint)  # привязываем кнопку к функции

        # создаём кнопку расчёта внутренней устойчивости графа
        self.internal_stability_button = wx.Button(self.panel, label="Внутренняя устойчивость", size=(190, 30))
        # создаём виджет кнопки
        self.internal_stability_button.Bind(wx.EVT_BUTTON, self.internal_stability)  # привязываем кнопку к функции

        # Размещаем виджеты на панели
        self.sizer = wx.BoxSizer(wx.VERTICAL)  # создаём общий sizer
        input_sizer = wx.BoxSizer(wx.VERTICAL)  # создаём sizer для input поля и кнопки создания таблицы
        input_sizer.Add(self.input_size, 0, wx.ALL, 5)  # добавляем в sizer поле input
        input_sizer.Add(self.size_table_button, 0, wx.ALL, 5)  # добавляем кнопку в sizer
        self.sizer.Add(input_sizer, 0, wx.ALL)  # добавляем sizer в общий sizer

        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)  # Добавляем таблицу в общий sizer

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # создаём sizer для кнопок
        button_sizer.Add(self.graph_button, 0, wx.BOTTOM, 5)  # добавляем в sizer кнопку отрисовки графа
        button_sizer.Add(self.internal_stability_button, 0, wx.BOTTOM, 5)  # добавляем в sizer кнопку
        button_sizer.Add(self.back_button, 0, wx.BOTTOM, 5)  # добавляем в sizer кнопку назад
        self.sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT)  # добавляем sizer в общий sizer

        # Скрываем не нужные виджеты на главной панели
        self.graph_button.Show(False)  # скрываем виджет кнопки отрисовки графа
        self.internal_stability_button.Show(False)  # скрываем виджет кнопки расчёта числа внутренней устойчивости графа
        self.back_button.Show(False)  # скрываем виджет кнопки назад
        self.grid.Show(False)  # скрываем виджет таблицы

        self.panel.SetSizer(self.sizer)  # отрисовываем виджеты на панели
        self.panel.Layout()  # размещаем виджеты в соответствии с их размерами

    def back_window(self, event) -> None:
        """ Метод event для кнопки назад"""
        self.delete_text_widget()  # удаляем виджет текста
        self.grid.ClearGrid()  # очищаем таблицу
        self.grid.Show(False)  # скрываем таблицу
        self.graph_button.Show(False)  # скрываем виджет кнопки отрисовки графа
        self.internal_stability_button.Show(False)  # скрываем виджет кнопки расчёта внутренней устойчивости графа
        self.back_button.Show(False)  # скрываем кнопку назад
        self.input_size.Show()  # показываем input поля для ввода размера таблицы
        self.size_table_button.Show()  # показываем кнопку создания таблицы

    def change_table_size(self, rows, cols) -> None:
        """ Метод для создания или изменения таблицы """
        if not self.grid.GetNumberRows():  # Если таблица еще не создана
            self.grid.CreateGrid(rows, cols)  # Создаём таблицу
        else:
            current_cols = self.grid.GetNumberCols()  # получаем кол-во колонок в текущей таблице
            current_rows = self.grid.GetNumberRows()  # получаем кол-во строк в текущей таблице
            if rows > current_rows:  # если строк в текущей таблице меньше чем задано
                self.grid.AppendRows(rows - current_rows)  # добавляем строки в текущую таблицу
            elif rows < current_rows:  # если строк в текущей таблице больше чем задано
                self.grid.DeleteRows(rows, current_rows - rows)  # удаляем строки в текущей таблице
            if cols > current_cols:  # если колонок в текущей таблице меньше чем задано
                self.grid.AppendCols(cols - current_cols)  # добавляем колонки в текущей таблицы
            elif cols < current_cols:  # если колонок в текущей таблице больше чем задано
                self.grid.DeleteCols(cols, current_cols - cols)  # удаляем колонки в текущей
        for row in range(rows):  # проходим по колонкам
            self.grid.SetRowLabelValue(row, f"x{row + 1}")  # именнуем строки в таблице как xi
            for col in range(cols):  # проходим по строкам
                self.grid.SetColLabelValue(col, f"x{col + 1}")  # именнуем каждую колонку xi
                self.grid.SetCellValue(row, col, "0")  # заполняем таблицу 0
                self.grid.SetCellBackgroundColour(row, col, wx.RED)

    def create_table(self, event) -> None:
        """Метод event для задания размерности таблицы
            и её создания при помощи функции change_table_size """
        self.delete_text_widget()  # удаляем виджет текста
        try:  # проверяем валидацию данных (корректные данные input поле являются данные типа int)
            value = int(self.input_size.GetValue())  # получаем значение из input поля
            if 1 < value <= 10:  # проверяем введённый размер таблицы (максимум она может быть 10х10 и минимум 2х2)
                self.change_table_size(value, value)  # создаём или изменяем существующую таблицу
                self.size_table_button.Show(False)  # cкрываем виджет кнопки создания таблицы
                self.input_size.Show(False)  # скрываем input виджет
                self.grid.Show(True)  # показываем виджет таблицы
                self.graph_button.Show(True)  # показываем виджет кнопки отрисовки графа
                self.internal_stability_button.Show(True)  # показываем виджет кнопки внутренней устойчивости
                self.back_button.Show(True)  # показываем виджет кнопки назад
                self.panel.Layout()  # размещаем виджеты с учётом их размерности
            else:
                # выводим сообщения об ошибке
                self.show_text("максимальная размерность таблицы 10x10 а минимальный 2x2")
                return
        except ValueError:  # в случае если значение не типа int то выводим сообщение об ошибке
            self.show_text("Введите целое число")
            return

    def cheek_vertex_and_create_matrix(self) -> tuple:
        """Метод для обработки таблицы смежности вершин графа
            и создании матрицы смежности графа с учётом валидации вершин"""
        vertex_list = list()  # создаём список связей вершин для построения попарных дизъюнкций
        vertex = list()  # создаём список всех вершин для проверки внутренней устойчивости графа
        grid = self.FindWindowByName("grid")  # Найти объект таблицы по имени
        vertex_matrix = [list() for _ in range(grid.GetNumberRows())]  # инициализируем матрицу смежности вершин
        for row in range(grid.GetNumberRows()):  # проходимся по строкам таблицы
            vertex.append(f"x{row + 1}")  # заполняем список вершин
            for col in range(grid.GetNumberCols()):  # проходимся по колонкам таблицы
                num = grid.GetCellValue(row, col)  # получаем значение из колонки
                if self.valid_vertex(num, row, col):  # проверяем валидны ли значения
                    # выбираем 2 связанные вершины
                    if int(num) == 1:
                        vertex_list.append((f"x{row + 1}", f"x{col + 1}"))  # добавляем связанные вершины в список связей вершин
                    vertex_matrix[row].append(int(num))  # добавляем элементы в матрицу смежности
                else:
                    vertex_list.clear()  # очищаем список связей вершин при ошибки валидации значений
        return vertex_list, vertex_matrix, vertex

    def internal_stability(self, event) -> None:
        """ Метод event для проверки связанности графа и
            и вычисления внутреннего числа устойчивости графа """
        self.delete_text_widget()  # удаляем виджет текста
        # получаем матрицу смежности вершин и список связей вершин
        vertex_list, vertex_matrix, vertex = self.cheek_vertex_and_create_matrix()
        if vertex_list and vertex_matrix and vertex:  # проверяем что списки не пустые
            if self.dfs_matrix(vertex_matrix):  # проверяем связанность вершин
                # вычисляем число внутренней устойчивости графа
                num_stability = internal_stability_num(vertex_list, len(vertex))
                # выводим число внутренней устойчивости графа
                self.show_text(f"Число внутренней устойчивости a(G) = {num_stability} ")
        return

    def dfs(self, matrix: list, vertex: int, visited: list) -> None:
        """ Рекурсивный метод обхода графа в глубину
            для определения связей вершин """
        visited[vertex] = True  # проверяем метку вершины
        for i in range(len(matrix[vertex])):  # проходимся по вершинам графа
            if matrix[vertex][i] == 1 and not visited[i]:  # если мы не посещали данную вершину
                self.dfs(matrix, i, visited)  # проверяем рекурсивно все связи вершины

    def dfs_matrix(self, vertex_matrix: list) -> bool:
        """ Метод определяющая связанность графа """
        visited = [False] * len(vertex_matrix)  # заполняем массив метками вершин
        for i in range(len(vertex_matrix)):  # проходимся по вершинам графа
            if not visited[i]:  # если вершина не посещена
                self.dfs(vertex_matrix, i, visited)  # выполняем функцию обхода графа в глубину
                if all(visited):  # если список состоит из всех меток посещённых вершин
                    return True
                else:
                    self.show_text("Граф не связанный или граф является ориентированным")
                    return False

    def show_text(self, message) -> None:
        """ Метод для отображения текста на панели """
        text = wx.StaticText(self.panel, label=message)  # создаём виджет текста
        self.sizer.Add(text, 0, wx.BOTTOM | wx.RIGHT | wx.ALIGN_RIGHT, 5)  # добавляем текстовый виджет в панель
        self.panel.Layout()

    def valid_vertex(self, num: str, row: int, col: int) -> bool:
        """ Метод валидации значений таблицы """
        num = int(num)  # получаем текущее значение по номеру колонки и столбцу
        if num != 0 and num != 1:  # если число не 1 или 0
            self.show_text("В таблице может быть только 0 или 1")
            return False
        elif row == col and num == 1:  # если существуют петли графа
            self.show_text("Число внутренней устойчивости расчитывается у графов без петель")
            return False
        return True

    def graph_paint(self, event) -> None:
        """ Метод event для отрисовки
            графа по связям вершин """
        self.delete_text_widget()  # удаляем виджет текста
        vertex_list, _, _ = self.cheek_vertex_and_create_matrix()  # получаем список связей вершин
        if vertex_list:  # проверяем что бы список связей не был пуст
            if nx.is_empty(self.G):  # проверяем был ли отрисован граф
                self.G.add_edges_from(vertex_list)  # добавляем связи вершин графа
                nx.draw(self.G, with_labels=True, font_weight='bold')  # рисуем граф
                plt.show()  # выводим граф на экран
            else:
                self.G.clear_edges()  # очищаем связи графа
                plt.clf()  # очищаем рисунок графа
        return

    def delete_text_widget(self) -> None:
        """ Метод удаления виджета текста """
        for child in self.panel.GetChildren():  # проходимся по списку виджетов панели
            if isinstance(child, wx.StaticText):  # проверяем есть ли среди виджетов виджет текста
                 child.Destroy()  # удаляем данный виджет с панели

    def color_value_table(self, event):
        """ Метод event для проверки и замены цвета в табличке """
        row = event.GetRow()  # получаем текущую строку
        col = event.GetCol()  # получаем текущую колонку

        value = self.grid.GetCellValue(row, col)  # получаем текущее значение из ячейки

        # Производим проверку условия
        if value == '1':
            self.grid.SetCellBackgroundColour(row, col, wx.GREEN)  # красим ячейку в зеленый
            self.grid.SetCellValue(row, col, '1')  # заменяем на 1
            self.grid.SetCellTextColour(row, col, wx.RED)  # красим 1 в красный
        else:
            self.grid.SetCellBackgroundColour(row, col, wx.RED)  # красим ячейку в красный
            self.grid.SetCellValue(row, col, '0')  # заменяем на 0
            self.grid.SetCellTextColour(row, col, wx.BLACK)  # красим 0 в чёрный


app = wx.App()  # создаём приложение
frame = WindowApp(None, title="Внутренняя устойчивость графа")  # создаём окно приложения с панелью
frame.Show()  # показываем наше окно
# создаём цикл событий
app.MainLoop()