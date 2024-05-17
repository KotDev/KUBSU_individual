import wx
from wx.grid import Grid
from polynomial import arr_x, arr_y, F


class WindowApp(wx.Frame):  # описываем базовый класс нашего окна
    def __init__(self, *args, **kw):
        """Инициализируем все виджеты и панель, получаем все методы и атрибуты унаследованного"""
        super(WindowApp, self).__init__(*args, **kw, size=(900, 400))

        self.panel = wx.Panel(self)  # создаём панель окна
        self.grid = Grid(self.panel)  # создаём таблицу

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.color_value_table)

        # создаём кнопку "принять" и input виджет
        self.size_table_button = wx.Button(self.panel, label="Принять", size=(100, 30))  # создаём виджет кнопки
        self.size_table_button.Bind(wx.EVT_BUTTON, self.create_table)  # привязываем кнопку к функции
        # создаём input виджет
        self.input_size = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=(300, -1))
        self.input_size.SetHint("Размерность таблицы 2 x n")

        # создаём кнопку назад
        self.back_button = wx.Button(self.panel, label="Назад", size=(100, 30))  # создаём виджет кнопки
        self.back_button.Bind(wx.EVT_BUTTON, self.back_window)  # привязываем кнопку к функции

        # создаём кнопку расчёта и создания полинома
        self.add_button = wx.Button(self.panel, label='полином', size=(100, 30))  # создаём виджет кнопки
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_button)  # привязываем кнопку к функции

        # Размещаем виджеты на панели
        self.sizer = wx.BoxSizer(wx.VERTICAL)  # создаём общий sizer
        input_sizer = wx.BoxSizer(wx.VERTICAL)  # создаём sizer для input поля и кнопки создания таблицы
        input_sizer.Add(self.input_size, 0, wx.EXPAND | wx.ALL, 5)  # добавляем в sizer поле input
        input_sizer.Add(self.size_table_button, 0, wx.EXPAND | wx.ALL, 5)  # добавляем кнопку в sizer
        self.sizer.Add(input_sizer, 0, wx.EXPAND)  # добавляем sizer в общий sizer

        self.sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)  # Добавляем таблицу в общий sizer

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # создаём sizer для кнопок
        button_sizer.Add(self.add_button, 0, wx.BOTTOM, 5)  # добавляем в sizer кнопку расчёта и создания полинома
        button_sizer.Add(self.back_button, 0, wx.BOTTOM, 5)  # добавляем в sizer кнопку назад
        self.sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT) # добавляем sizer в общий sizer

        # Скрываем не нужные виджеты на главной панели
        self.add_button.Show(False)  # скрываем виджет кнопки расчёта и создания полинома
        self.back_button.Show(False)  # скрываем виджет кнопки назад
        self.grid.Show(False)  # скрываем виджет таблицы

        self.panel.SetSizer(self.sizer)  # отрисовываем виджеты на панели

    def back_window(self, event) -> None:
        """ Метод event для кнопки назад"""
        self.delete_text_widget()  # удаляем виджет текста
        self.grid.ClearGrid()  # очищаем таблицу
        self.grid.Show(False)  # скрываем таблицу
        self.add_button.Show(False)  # скрываем виджет кнопки создания и расчёта полинома
        self.back_button.Show(False)  # скрываем кнопку назад
        self.input_size.Show()  # показываем input поля для ввода размера таблицы
        self.size_table_button.Show()  # показываем кнопку создания таблицы

    def change_table_size(self, rows, cols):
        """ Метод для создания или изменения таблицы """
        if not self.grid.GetNumberRows():  # Если таблица еще не создана
            self.grid.CreateGrid(rows, cols)  # Создаём таблицу
            self.grid.SetRowLabelValue(0, "x")  # именнуем 1 строку в таблице как x
            self.grid.SetRowLabelValue(1, "y")  # именнуем 2 строку в таблице как y
        else:
            current_cols = self.grid.GetNumberCols()  # получаем кол-во колонок в текущей таблице
            if cols > current_cols:  # если колонок в текущей таблице меньше чем задано
                self.grid.AppendCols(cols - current_cols)  # добавляем колонки в текущей таблицы
            elif cols < current_cols:  # если колонок в текущей таблице больше чем задано
                self.grid.DeleteCols(cols, current_cols - cols)  # удаляем колонки в текущей
        for row in range(rows):  # проходим по колонкам
            for col in range(cols):  # проходим по строкам
                self.grid.SetColLabelValue(col, f"{col + 1}")  # именнуем каждую колонку цифрой
                self.grid.SetCellValue(row, col, "0")  # заполняем таблицу 0
                self.grid.SetCellBackgroundColour(row, col, wx.RED)

    def create_table(self, event) -> None:
        """Метод event для задания размерности таблицы
            и её создания при помощи функции change_table_size """
        self.delete_text_widget()  # удаляем виджет текста
        try:  # проверяем валидацию данных (корректные данные input поле являются данные типа int)
            value = int(self.input_size.GetValue())  # получаем значение из input поля
            if 1 < value <= 10:  # проверяем введёный размер таблицы (максимум она может быть 2х10 и минимум 2х2)
                self.change_table_size(2, value)  # создаём или изменяем существующую таблицу
                self.size_table_button.Show(False)  # cкрываем виджет кнопки создания таблицы
                self.input_size.Show(False)  # скрываем input виджет
                self.grid.Show(True)  # показываем виджет таблицы
                self.add_button.Show(True)  # показываем виджет кнопки расчёта и создания полинома
                self.back_button.Show(True)  # показываем виджет кнопки назад
                self.panel.Layout()
            else:
                self.show_text("максимальная размерность таблицы 2x10 а минимальный 2x2")  # выводим сообщения об ошибке
                return
        except ValueError:  # в случае если значение не типа int то выводим сообщение об ошибке
            self.show_text("Введите целое число")
            return

    def on_add_button(self, event) -> None:
        """Метод event для вывода значений f(x) = y
            и создании интерполяционного полинома Лагранжа"""
        self.delete_text_widget()  # удаляем виджет текста
        grid = self.FindWindowByName("grid")  # Найти объект таблицы по имени
        for row in range(grid.GetNumberRows()):  # проходимся по строкам таблицы
            for col in range(grid.GetNumberCols()):  # проходимся по колонкам таблицы
                try:  # проверяем валидацию данных в таблице (все данные таблицы должны быть типа int)
                    num = int(grid.GetCellValue(row, col))  # получаем текущее значение по номеру колонки и столбцу
                    if not row:  # если строка с индексом 0 т.е строка x
                        arr_x.append(num)  # добавляем в список состоящий из элементов x наше значение из таблицы
                    else:
                        arr_y.append(num)  # добавляем в список состоящий из элементов y наше значение из таблицы
                except ValueError:  # если элемент таблицы не является типом данных int то показываем текст ошибки
                    self.show_text("Ошибка валидации")  # текст ошибки
                    arr_x.clear()  # очищаем заполненный массив из элементов x
                    arr_y.clear()  # очищаем заполненный массив из элементов y
                    # это надо что бы при повторном нажатии кнопки расчёта и создания полинома списки были пусты
                    return
        if all((x == 0 for x in arr_x)) or all((y == 0 for y in arr_y)):  # проверяем что бы оба списка были не 0
            arr_x.clear()  # очищаем заполненный массив из элементов x
            arr_y.clear()  # очищаем заполненный массив из элементов y
            self.show_text("Одна из строк состоит из нулей")  # выдаём сообщение об ошибки
            return
        polynom = ""  # создаём переменную для вывода полинома
        for x in arr_x:  # проходимся по элементам массива x
            res = F(x)  # создаём полином и получаем значение f(x)
            polynom = res[1] # записываем наш созданный полином в переменную
            self.show_text(f"F({x}) = {res[0]}")  # выводим текст со значением функции f(x) = y
        polynom = str(polynom).replace("**", "^")
        self.show_text(f"F(x) = {polynom}")  # выводим сам интерполяционный полином Лагранжа
        print(f"F(x) = {polynom}")
        arr_x.clear()  # очищаем список x
        arr_y.clear()  # очищаем список y

    def show_text(self, message) -> None:
        """ Метод для отображения текста на панели """
        text = wx.StaticText(self.panel, label=message)  # создаём виджет текста
        self.sizer.Add(text, 0, wx.BOTTOM | wx.RIGHT | wx.ALIGN_RIGHT, 5)  # добавляем текстовый виджет в панель
        self.panel.Layout()

    def delete_text_widget(self) -> None:
        """ Метод удаления виджета текста"""
        for child in self.panel.GetChildren():  # проходимся по списку виджетов панели
            if isinstance(child, wx.StaticText):  # проверяем есть ли среди виджетов виджет текста
                 child.Destroy()  # удаляем данный виджет с панели

    def color_value_table(self, event):
        """ Метод event для проверки и замены цвета в табличке """
        row = event.GetRow()  # получаем текущую строку
        col = event.GetCol()  # получаем текущую колонку

        value = self.grid.GetCellValue(row, col)  # получаем текущее значение из ячейки

        # Производим проверку условия
        if value != '0':
            self.grid.SetCellBackgroundColour(row, col, wx.GREEN)  # красим ячейку в зеленый
            self.grid.SetCellValue(row, col, value)  # заменяем на value
            self.grid.SetCellTextColour(row, col, wx.RED)  # красим 1 в красный
        else:
            self.grid.SetCellBackgroundColour(row, col, wx.RED)  # красим ячейку в красный
            self.grid.SetCellValue(row, col, '0')  # заменяем на 0
            self.grid.SetCellTextColour(row, col, wx.BLACK)  # красим 0 в чёрный



app = wx.App()  # создаём приложение
frame = WindowApp(None, title="Полином Лагранжа")  # создаём окно приложения с панелью
frame.Show()  # показываем наше окно
# создаём цикл событий
app.MainLoop()