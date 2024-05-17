import ast
import wx
from complex_operation import ComplexOperation, ComplexForm, ComplexFormTranslation


class WindowApp(wx.Frame):  # описываем базовый класс нашего окна
    def __init__(self, *args, **kw):
        """Инициализируем все виджеты и панель, получаем все методы и атрибуты унаследованного класса"""
        super(WindowApp, self).__init__(*args, **kw, size=(900, 400))

        self.panel = wx.Panel(self)  # создаём панель окна

        # Создаём кнопку операции для операций над комплексными числами
        self.operation_button = wx.Button(self.panel, label="Операции", size=(200, 100))
        # Присваиваем к кнопке функцию event
        self.operation_button.Bind(wx.EVT_BUTTON, self.on_operation)
        # Перекрашиваем кнопку и цвет текста в кнопке
        self.operation_button.SetBackgroundColour(wx.Colour(212, 212, 212))
        self.operation_button.SetForegroundColour(wx.Colour(0,0,0))

        # Создаём кнопку операции для представлении комплексного числа
        self.form_button = wx.Button(self.panel, label="Представление в виде", size=(200, 100))
        # Присваиваем к кнопке функцию event
        self.form_button.Bind(wx.EVT_BUTTON, self.on_form)
        # Перекрашиваем кнопку и цвет текста в кнопке
        self.form_button.SetBackgroundColour(wx.Colour(212, 212, 212))
        self.form_button.SetForegroundColour(wx.Colour(0, 0, 0))

        # Создаём кнопку операции для представлении из формы комплексного числа
        self.form_translate_button = wx.Button(self.panel, label="Представление из", size=(200, 100))
        # Присваиваем к кнопке функцию event
        self.form_translate_button.Bind(wx.EVT_BUTTON, self.on_form_translate)
        # Перекрашиваем кнопку и цвет текста в кнопке
        self.form_translate_button.SetBackgroundColour(wx.Colour(212, 212, 212))
        self.form_translate_button.SetForegroundColour(wx.Colour(0, 0, 0))

        # Создаём input поля для ввода комплексных чисел
        # input поле комплексного числа а
        self.input_complex_a = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=(50, -1))
        # input поле комплексного числа b
        self.input_complex_b = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=(50, -1))
        # input поле для ввода целочисленной степени
        self.input_degree = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=(50, -1))
        # input поле для ввода аргумента комплексного числа
        self.input_arg = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=(50, -1))
        # input поле для модуля комплексного числа
        self.input_module = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER | wx.TE_NO_VSCROLL, size=(50, -1))

        # создаём кнопку назад
        self.back_button = wx.Button(self.panel, label="Назад", size=(200, 100))  # создаём виджет кнопки
        self.back_button.Bind(wx.EVT_BUTTON, self.back_window)  # привязываем кнопку к функции event
        # задаём цвет кнопке и её тексту
        self.back_button.SetBackgroundColour(wx.Colour(212, 212, 212))
        self.back_button.SetForegroundColour(wx.Colour(0, 0, 0))

        # Создаём кнопку для расчёта опарации над комплексными числами
        self.confirm_operation = wx.Button(self.panel, label="Расчитать", size=(200, 100))
        # Присваиваем к кнопке функцию event
        self.confirm_operation.Bind(wx.EVT_BUTTON, self.on_confirm_operation)
        # Перекрашиваем кнопку и цвет текста в кнопке
        self.confirm_operation.SetBackgroundColour(wx.Colour(212, 212, 212))
        self.confirm_operation.SetForegroundColour(wx.Colour(0,0,0))

        # Создаём кнопку для представления комплексного числа в какой либо форме
        self.confirm_operation_from = wx.Button(self.panel, label="Представить", size=(200, 100))
        # Присваиваем к кнопке функцию event
        self.confirm_operation_from.Bind(wx.EVT_BUTTON, self.on_confirm_operation_from)
        # Перекрашиваем кнопку и цвет текста в кнопке
        self.confirm_operation_from.SetBackgroundColour(wx.Colour(212, 212, 212))
        self.confirm_operation_from.SetForegroundColour(wx.Colour(0,0,0))

        # Создаём кнопку для представления комплексного числа из одной формы в другую
        self.confirm_operation_from_translate = wx.Button(self.panel, label="Представить в", size=(200, 100))
        # Присваиваем к кнопке функцию event
        self.confirm_operation_from_translate.Bind(wx.EVT_BUTTON, self.on_confirm_operation_from_translate)
        # Перекрашиваем кнопку и цвет текста в кнопке
        self.confirm_operation_from_translate.SetBackgroundColour(wx.Colour(212, 212, 212))
        self.confirm_operation_from_translate.SetForegroundColour(wx.Colour(0,0,0))

        # указываем список последовательности операции
        choices_operations = ["Сложить", "Вычесть", "Умножить", "Разделить"]
        # создаём виджет choices
        self.choice_operation_complex = wx.Choice(self.panel, choices=choices_operations, size=(300, -1))

        # указываем список последовательности операции перевода
        choices_form = ["Экспоненциальная", "Тригонометрическая", "Возвести в степень"]
        # создаём виджет choices
        self.choice_operation_form = wx.Choice(self.panel, choices=choices_form, size=(300, -1))

        # указываем список последовательности операции перевода
        choices_from_translate = ["Тригонометрическая-экспоненциальная", "Тригонометрическая-алгебраическая",
                                  "Экспоненциальная-алгебраическая", "Экспоненциальная-тригонометрическая"]
        # создаём виджет choices
        self.choice_operation_from_translate = wx.Choice(self.panel, choices=choices_from_translate, size=(300, -1))


        # Размещаем виджеты на панели
        self.sizer = wx.BoxSizer(wx.VERTICAL)  # создаём общий sizer

        input_sizer = wx.BoxSizer(wx.VERTICAL)  # создаём sizer для input поля
        input_sizer.Add(self.input_complex_a, 0, wx.EXPAND | wx.ALL, 5)  # добавляем в sizer поле input
        input_sizer.Add(self.input_complex_b, 0, wx.EXPAND | wx.ALL, 5)  # добавляем в sizer поле input
        input_sizer.Add(self.input_degree, 0, wx.EXPAND | wx.ALL, 5) # добавляем в sizer поле input
        input_sizer.Add(self.input_arg, 0, wx.EXPAND | wx.ALL, 5)  # добавляем в sizer поле input
        input_sizer.Add(self.input_module, 0, wx.EXPAND | wx.ALL, 5)  # добавляем в sizer поле input
        self.sizer.Add(input_sizer, 0, wx.EXPAND)  # добавляем sizer в общий sizer

        choices_sizer = wx.BoxSizer(wx.HORIZONTAL)  # создаём sizer для виджета choices
        choices_sizer.Add(self.choice_operation_complex, 0, wx.ALL, 5)  # добавляем в sizer виджет choices
        choices_sizer.Add(self.choice_operation_form, 0, wx.ALL, 5)  # добавляем в sizer виджет choices
        choices_sizer.Add(self.choice_operation_from_translate, 0, wx.ALL, 5)  # добавляем в sizer виджет choices
        self.sizer.Add(choices_sizer, 0, wx.EXPAND | wx.ALL, 5)  # добавляем sizer в общий sizer

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # создаём sizer для кнопок
        button_sizer.Add(self.operation_button, 0, wx.ALL, 10)  # добавляем кнопку в sizer
        button_sizer.Add(self.form_button, 0, wx.CENTER, 10)  # добавляем кнопку в sizer
        button_sizer.Add(self.form_translate_button, 0, wx.ALL, 10)  # добавляем кнопку в sizer
        self.sizer.Add(button_sizer, 0, wx.CENTER)  # добавляем sizer в общий sizer

        button_sizer_operations = wx.BoxSizer(wx.HORIZONTAL)  # добавляем sizer кнопок операций
        button_sizer_operations.Add(self.confirm_operation, 0, wx.BOTTOM, 5)  # добавляем кнопку в sizer
        button_sizer_operations.Add(self.confirm_operation_from, 0, wx.BOTTOM, 5)  # добавляем кнопку в sizer
        button_sizer_operations.Add(self.confirm_operation_from_translate, 0, wx.BOTTOM, 5)  # добавляем кнопку в sizer
        button_sizer_operations.Add(self.back_button, 0, wx.BOTTOM, 50)  # добавляем кнопку в sizer
        self.sizer.Add(button_sizer_operations, 0, wx.ALIGN_RIGHT)  # добавляем sizer в общий sizer

        # Скрываем не нужные виджеты на главной панели
        self.input_degree.Show(False)  # скрываем виджет ввода степени
        self.input_complex_a.Show(False)  # скрываем виджет ввода комплексного числа а
        self.input_complex_b.Show(False)  # скрываем виджет ввода комплексного числа b
        self.choice_operation_complex.Show(False)  # скрываем виджет последовательности операции
        self.choice_operation_form.Show(False)  # скрываем виджет последовательности операций перевода
        self.back_button.Show(False)  # скрываем виджет кнопки назад
        self.confirm_operation.Show(False)  # скрываем виджет кнопки расчёта
        self.confirm_operation_from.Show(False)  # скрываем виджет кнопки представить в
        self.choice_operation_from_translate.Show(False)  # скрываем виджет кнопки представить из
        self.input_module.Show(False)  # скрываем виджет ввода модуля комплексного числа
        self.input_arg.Show(False)  # скрываем виджет ввода аргумента комплексного числа

        self.panel.SetSizer(self.sizer)  # отрисовываем виджеты на панели

    def back_window(self, event) -> None:
        """ Метод event для кнопки назад"""
        self.input_degree.Show(False)  # скрываем поле ввода степени
        self.delete_text_widget()  # удаляем виджет текста
        self.show_widget_on_operation(True)  # показываем виджеты главного окна
        self.show_widget_input_on_operation(False)  # скрываем виджеты окна операций над комплексными числами
        self.show_widget_input_on_form(False)  # скрываем виджеты окна представления в форме
        # скрывем виджеты окна представления комплексного числа из одной формы в другую
        self.show_widget_input_from_on_translate(False)

    def on_operation(self, event):
        """Метод event для окна операций над комплексными числами"""
        self.input_degree.Show(False)  # скрываем поле ввода в сепень
        self.show_widget_on_operation(False)  # скрываем виджет главного окна
        self.show_widget_input_on_operation(True)  # показывам виджеты окна операций над комплексными числами

    def on_form(self, event):
        """Метод event для окна представления комплексного числа"""
        self.input_degree.Show(False)  # скрываем виджет ввода степени
        self.show_widget_on_operation(False)  # скрываем виджет главного окна
        self.show_widget_input_on_form(True)  # показываем виджеты окна представления в форме

    def on_form_translate(self, event):
        """Метод event для окна представления комплексного числа из одной формы в другую"""
        self.input_degree.Show(False)  # скрываем виджет ввода степени
        self.show_widget_on_operation(False)  # скрываем виджет главного окна
        # показываем виджеты окна представления комплексного числа из одной формы в другую
        self.show_widget_input_from_on_translate(True)

    def on_confirm_operation_from(self, event):
        """Метод event представления комплексного числа в выбранной форме"""
        self.delete_text_widget()  # удаляем текст
        res_choice = self.choice_operation_form.GetStringSelection()  # получаем операцию которую выбрал пользователь
        a = self.input_complex_a.GetValue()  # получаем число из поля ввода комплексного числа a
        degree = self.input_degree.GetValue() # получсаем число из поля ввода степени комплексного числа
        if self.complex_validator(a):  # проверяем комплексное число на корректность
            a = complex(ast.literal_eval(a))  # переводим введённое комплексное число в тип complex
        else:
            self.show_text("Введите комплексное число")  # выдаём ошибку о некоректности данных
            return
        form = ComplexForm(a)  # представляем комплексное число в нужную форму
        if res_choice == "Возвести в степень":  # если пользователь выбрал операцию возведения в степень
            self.input_degree.Show()  # показать виджет ввода сепени числа
            if self.int_validator(degree):  # проверить степень на корректность
                self.show_text(f"{form.degree_complex_num(int(degree))}")  # вывод выбранной формы на экран
            else:
                self.show_text("Введите целое число")  # выводим ошибку о корректности ввода степени числа
        else:
            self.input_degree.Show(False)  # скрывем виджет ввода степени числа
            self.input_degree.Clear()  # очищаем данный виджет
            match res_choice:  # сверяем выбранную операцию
                case "Экспоненциальная":
                    return self.show_text(f"{form.expan_complex_form()}")  # вывод выбранной формы на экран
                case "Тригонометрическая":
                    return  self.show_text(f"{form.trig_complex_form()}")  # вывод выбранной формы на экран
                case _:
                    # вывод ошибки если пользователь не выбрал ни одну оперцию
                    return self.show_text("Вы забыли выбрать форму представления")

    def on_confirm_operation(self, event):
        """Метод event для вычисления выбранной операции над комплексными числами а и b"""
        self.delete_text_widget()  # удаляем текст
        a = self.input_complex_a.GetValue()  # получаем значение поля ввода комплексного числа a
        b = self.input_complex_b.GetValue()  # получаем значение поля ввода комплексного числа b
        if self.complex_validator(a) and self.complex_validator(b):  # Проверяем комплексные числа на корректность
            a = complex(ast.literal_eval(a))  # переводим введённое комплексное a число в тип complex
            b = complex(ast.literal_eval(b))  # переводим введённое комплексное b число в тип complex
            # получаем форму которую выбрал пользователь
            res_choice = self.choice_operation_complex.GetStringSelection()
            operations = ComplexOperation(a, b)  # выполняем операцию над комплексным числом
            match res_choice:
                case "Сложить":
                    return self.show_text(f"{operations.fold_complex_num()}")
                case "Умножить":
                    return self.show_text(f"{operations.multiplication_complex_num()}")
                case "Разделить":
                    return self.show_text(f"{operations.division_complex_num()}")
                case "Вычесть":
                    return self.show_text(f"{operations.difference_complex_num()}")
                case _:
                    self.show_text("Вы забыли выбрать операцию")
        else:
            self.show_text("Введите комплексное число")

    def on_confirm_operation_from_translate(self, event):
        self.delete_text_widget()
        arg = self.input_arg.GetValue()
        module = self.input_module.GetValue()
        res_choice = self.choice_operation_from_translate.GetStringSelection()
        if self.int_validator(arg) and self.int_validator(module):
            arg = int(ast.literal_eval(arg))
            module = float(ast.literal_eval(module))
            form_translate = ComplexFormTranslation(arg, module)
            match res_choice:
                case "Тригонометрическая-экспоненциальная":
                    return self.show_text(f"{form_translate.trig_expan_complex_form()}")
                case "Тригонометрическая-алгебраическая":
                    return self.show_text(f"{form_translate.trig_algebra_complex_form()}")
                case "Экспоненциальная-алгебраическая":
                    return self.show_text(f"{form_translate.expan_algebra_complex_form()}")
                case "Экспоненциальная-тригонометрическая":
                    return self.show_text(f"{form_translate.expan_trig_complex_form()}")
                case _:
                    return self.show_text("Вы забыли выбрать операцию")
        else:
            self.show_text("Аргумент должен быть N числом а модуль должен быть R числом")

    def complex_validator(self, value):
        try:
            ast.literal_eval(value)
            return True
        except (ValueError, SyntaxError):
            return False

    def int_validator(self, value):
        try:
            int(ast.literal_eval(value))
            return True
        except (ValueError, SyntaxError, TypeError):
            return False

    def show_widget_on_operation(self, flag):
        self.operation_button.Show(flag)
        self.form_button.Show(flag)
        self.form_translate_button.Show(flag)
        self.panel.Layout()

    def show_widget_input_on_operation(self, flag):
        self.input_complex_a.Show(flag)
        self.input_complex_b.Show(flag)
        self.confirm_operation.Show(flag)
        self.back_button.Show(flag)
        self.choice_operation_complex.Show(flag)
        self.input_complex_a.Clear()
        self.input_complex_b.Clear()
        self.input_complex_a.SetHint("Введите комплексное число а")
        self.input_complex_b.SetHint("Введите комплексное число b")
        self.panel.Layout()

    def show_widget_input_on_form(self, flag):
        self.input_complex_a.Show(flag)
        self.confirm_operation_from.Show(flag)
        self.choice_operation_form.Show(flag)
        self.back_button.Show(flag)
        self.input_complex_a.Clear()
        self.input_degree.Clear()
        self.input_complex_a.SetHint("Введите комплексное число а")
        self.input_degree.SetHint("Целую степень")
        self.panel.Layout()

    def show_widget_input_from_on_translate(self, flag):
        self.input_module.Show(flag)
        self.input_arg.Show(flag)
        self.back_button.Show(flag)
        self.confirm_operation_from_translate.Show(flag)
        self.choice_operation_from_translate.Show(flag)
        self.input_arg.Clear()
        self.input_module.Clear()
        self.input_arg.SetHint("Введите аргумент комплексного числа в градусах")
        self.input_module.SetHint("Введите модуль комплексного числа")
        self.panel.Layout()

    def show_text(self, message) -> None:
        """ Метод для отображения текста на панели """
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        text = wx.StaticText(self.panel, label=message)  # создаём виджет текста
        text.SetFont(font)
        self.sizer.Add(text, 0, wx.BOTTOM | wx.RIGHT | wx.ALIGN_RIGHT, 5)  # добавляем текстовый виджет в панель
        self.panel.Layout()

    def delete_text_widget(self) -> None:
        """ Метод удаления виджета текста"""
        for child in self.panel.GetChildren():  # проходимся по списку виджетов панели
            if isinstance(child, wx.StaticText):  # проверяем есть ли среди виджетов виджет текста
                 child.Destroy()  # удаляем данный виджет с панели


app = wx.App()  # создаём приложение
frame = WindowApp(None, title="Комплексные числа")  # создаём окно приложения с панелью
frame.Show()  # показываем наше окно
# создаём цикл событий
app.MainLoop()