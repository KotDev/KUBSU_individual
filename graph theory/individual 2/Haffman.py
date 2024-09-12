import matplotlib.pyplot as plt
import time


class RootTree:  # Класс корня дерева
    def __init__(self, left, right, value: int, info: str):
        self.left = left  # атрибут левой ветки
        self.right = right  # атрибут правой ветки
        self.value = value  # кол-во вхождений
        self.info = info  # символы

    def __repr__(self):  # метод для удобного вывода класса корня
        return f"({self.info})"


class HaffmanTree:  # класс дерева Хаффмана
    def __init__(self, text: str):
        self.text = text  # текст который хотим закодировать

    def frequency_analysis(self) -> list:  # метод для построения таблицы частот
        """
        Помечаем каждый символ списка как корень нашего дерева
        сортируем наш список корней в приоритете по частоте символа
        в порядке возрастаний. а после по символу в порядке возрастания по коду в ASCII
        """
        return sorted([RootTree(left=None, right=None,
                                value=self.text.count(i), info=f"{i}")
                       for i in set(self.text)], key=lambda x: (x.value, x.info))

    @staticmethod
    def build_tree(analysis_list: list) -> RootTree:  # метод создания дерева Хаффмана
        while len(analysis_list) > 1:  # пока в списке не остался единственный корень
            min_sim_1 = analysis_list[0]  # берём 1 минимальный корень в списке
            min_sim_2 = analysis_list[1]  # берём 2 минимальный корень в сриске
            # создаём корень дерева из 2х минимальный кореней в списке
            root = RootTree(left=min_sim_1, right=min_sim_2,
                            value=min_sim_1.value + min_sim_2.value,
                            info=f"{min_sim_1.info + ' ' + min_sim_2.info}")
            analysis_list.pop(0)  # удаляем 1 корень из списка корней
            analysis_list.pop(0)  # удаляем 2 корень из списка корней
            analysis_list.append(root)  # добавляем новый корень который связывает уже 2 элемента в списке
            # заново сортируем список корней
            analysis_list = sorted(analysis_list, key=lambda x: (x.value, x.info))
        return root # возвращаем главный корень дерева

    def view_tree(self, root: RootTree, x, y, level, parent_x=None, parent_y=None, edge_label=""):
        #  метод для отрисовки дерева
        if not root:
            return

        plt.text(x, y, str(root.value), style='italic')

        dx = 2.5 / (2 ** level)
        dy = 1.5

        if parent_x is not None and parent_y is not None:
            plt.plot([parent_x, x], [parent_y, y], 'ko-', lw=1.5, markersize=5, color='black')
            plt.text((x + parent_x) / 2, (y + parent_y) / 2,
                     edge_label, color='black', va='bottom', ha='center', zorder=2)

        text_to_display = str(root.value) + '\n' + root.info if parent_x is not None else str(root.value)

        plt.text(x, y, text_to_display, style='italic', weight='bold', size=12, ha='center', va='center',
                 bbox=dict(facecolor='lightgray', alpha=0.5, edgecolor='black', zorder=2))

        if root.left:
            self.view_tree(root.left, x - dx, y - dy, level + 1, x, y, "0")

        if root.right:
            self.view_tree(root.right, x + dx, y - dy, level + 1, x, y, "1")

    def save_image_tree(self, root_tree: RootTree, arg_path: str):
        # метод для сохранения фото рисованного дерева
        current_time = int(time.time())  # получаем текущее время для создания уникального пути изображения
        plt.figure(figsize=(8, 8))  # задаём размер фигуре
        self.view_tree(root_tree, 0, 0, 0, "")  # отрисовываем дерево
        plt.axis('off')
        plt.savefig(f'/home/danil/PycharmProjects/KUBSU_ndividual/graph theory/individual 2/tree_{arg_path}_image_{current_time}.png',
                    format='png')  # сохраняем фото по указанному пути
        return current_time


class Encoder(HaffmanTree):  # класс кодировки сообщения
    def __init__(self, text: str, table):
        super().__init__(text)  # наследуем атрибут текста из класса дерева Хаффмана
        self.table = table  # атрибут таблицы Хаффмана
        self.text = text

    def table_haffman(self, root: RootTree, code: str):  # метод создания таблицы Хаффмана
        if root is None:  # пока существует узел
            return

        if root.left is None and root.right is None: # если данный узел является липестком
            self.table[root.info] = code  # записываем полученный код в таблицу

        self.table_haffman(root.left, code + "0")  # проходим по левому узлу
        self.table_haffman(root.right, code + "1")  # проходим по правому узлу

    def encoder_text(self):  # метод закодирования сообщения при помощи таблицы
        code = ""
        if not self.table:  # если таблица пуста то код построить не возможно
            return ""

        for sim in self.text:  # проходимся по искомому тексту
            code += self.table[sim]  # кодируем символ в соответствии с таблицей
        return code

    def file_table_write(self, filename, code):  # метод записи таблицы Хаффмана в файл
        with open(filename, "w", encoding="utf-8") as file:
            file.write("-----------------------\n")
            for char, code in self.table.items():
                file.write(f"{char} - {code}\n")
            file.write("-----------------------\n")
            file.write("\n")
            file.write(f"Закодированный текст: {code}")

    def view_table(self):  # метод представления таблицы Хаффмана в виде текста
        table_text = ""
        table_text += "-----------------------\n"
        for char, code in self.table.items():
            table_text += f"{char} - {code}\n"
        table_text += "-----------------------\n"
        return table_text


class Decoder:  # класс декодирования сообщения
    def __init__(self, encoded_tex: str):
        self.encoded_tex = encoded_tex  # атрибут кодированного сообщения

    def decode(self, root):  # метод декодирования сообщения по дереву Хаффмана
        decoded_text = ""  # декодированный текст
        current_root = root  # берем корень дерева
        for bit in self.encoded_tex: # проходимся по каждому биту в кодировке
            if bit == "0":
                current_root = current_root.left  # если бит = 0 то идём по левой ветке
            else:
                current_root = current_root.right  # в противном случае проходимся по правой
            if len(current_root.info) == 1:  # если в корне дерева 1 символ то это лист
                decoded_text += current_root.info  # значение листа конкатенируем со строкой декодированного текста
                current_root = root  # возвращаемся в корень дерева
        return decoded_text



