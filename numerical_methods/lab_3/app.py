import sys

from PyQt5.QtCore import QMetaMethod
from PyQt5.QtWidgets import QTableWidgetItem

from window_app import Ui_MainWindow
from PyQt5 import QtWidgets
from slau import Slau

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, rows: int, cols: int):
        super().__init__()
        self.setupUi(self)
        self.rows = rows
        self.cols = cols
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        self.tableWidget_2.setRowCount(rows)
        self.tableWidget_2.setColumnCount(1)
        self.pushButton.clicked.connect(self.push)
        self.radioButton.clicked.connect(self.runing_r)
        self.radioButton_2.clicked.connect(self.gaus_r)
        self.gaus = False
        self.runing = False

    def push(self):
        print(self.gaus, self.runing)
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item is None:
                    return
        matrix: list[list[float]] = list()
        result: list[float] = [float(self.tableWidget_2.item(i, 0).text()) for i in range(self.rows)]
        for i in range(self.rows):
            matrix.append([float(self.tableWidget.item(i, j).text()) for j in range(self.cols)])
        self.tableWidget_2.clear()
        self.tableWidget.clear()
        self.textBrowser.clear()
        slau = Slau(matrix, result)
        if self.gaus:
            slau.method_gaus()
            self.textBrowser.setText(", ".join(map(str, slau.result)))
            for i in range(len(slau.matrix)):
                for j in range(len(slau.matrix[i])):
                    item = QtWidgets.QTableWidgetItem(str(matrix[i][j]))
                    self.tableWidget.setItem(i, j, item)
        elif self.runing:
            slau.method_gaus()
            self.textBrowser.setText(", ".join(map(str, slau.result)))
        else:
            self.textBrowser.setText("Метод не выбран")

    def gaus_r(self):
        self.runing = False
        self.gaus = True

    def runing_r(self):
        self.runing = True
        self.gaus = False


def main():
    row: int = int(input("Введите кол-во строк "))
    col: int = int(input("Введите кол-во колонок "))
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App(rows=row, cols=col)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()