import sys

from PyQt5.QtCore import QMetaMethod
from PyQt5.QtWidgets import QTableWidgetItem

from window_app import Ui_MainWindow
from PyQt5 import QtWidgets
from slau import SlauIteration

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
        self.radioButton.clicked.connect(self.relax_r)
        self.radioButton_2.clicked.connect(self.zeidel_r)
        self.relax = False
        self.zeidel = False

    def push(self):
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item is None:
                    return
        matrix: list[list[float]] = list()
        result: list[float] = [float(self.tableWidget_2.item(i, 0).text()) for i in range(self.rows)]
        w: float = self.lineEdit_2.text()
        epsilon: float = self.lineEdit.text()
        try:
            if w:
                w = float(w)
            epsilon = float(epsilon)
        except ValueError():
            self.tableWidget_2.clear()
            self.tableWidget.clear()
            self.textBrowser.clear()
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.textBrowser.setText("Вы не ввели epsilon")
        for i in range(self.rows):
            matrix.append([float(self.tableWidget.item(i, j).text()) for j in range(self.cols)])
        self.tableWidget_2.clear()
        self.tableWidget.clear()
        self.textBrowser.clear()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        slau = SlauIteration(matrix, result, x_pr=[0]*len(matrix), epsilon=epsilon, w=w)
        if self.zeidel:
            slau.zeidel()
            self.textBrowser.setText(", ".join(map(str, slau.x_pr)))
        elif self.relax:
            slau.relax_method()
            self.textBrowser.setText(", ".join(map(str, slau.x_pr)))
        else:
            self.textBrowser.setText("Метод не выбран")

    def zeidel_r(self):
        self.relax = False
        self.zeidel = True

    def relax_r(self):
        self.relax = True
        self.zeidel = False


def main():
    row: int = int(input("Введите кол-во строк "))
    col: int = int(input("Введите кол-во колонок "))
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App(rows=row, cols=col)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()