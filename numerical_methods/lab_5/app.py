import sys
from numerical_methods.lab_5.window_app import Ui_MainWindow
from PyQt5 import QtWidgets
from iterations_methods import Iterations

class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, rows: int, cols: int):
        super().__init__()
        self.setupUi(self)
        self.rows = rows
        self.cols = cols
        self.tableWidget_3.setRowCount(rows)
        self.tableWidget_3.setColumnCount(cols)
        self.pushButton.clicked.connect(self.push)
        self.jakobi.clicked.connect(self.jakobi_r)
        self.power_iteration.clicked.connect(self.power_r)
        self.jakobi_up = False
        self.power_up = False

    def push(self):
        for row in range(self.tableWidget_3.rowCount()):
            for col in range(self.tableWidget_3.columnCount()):
                item = self.tableWidget_3.item(row, col)
                if item is None:
                    return
        matrix: list[list[float]] = list()
        epsilon: float = self.lineEdit.text()
        try:
            epsilon = float(epsilon)
        except ValueError():
            self.tableWidget.clear()
            self.textBrowser.clear()
            self.lineEdit.clear()
            self.textBrowser.setText("Вы не ввели epsilon")
        for i in range(self.rows):
            matrix.append([float(self.tableWidget_3.item(i, j).text()) for j in range(self.cols)])
        self.tableWidget_3.clear()
        self.textBrowser.clear()
        self.lineEdit.clear()
        iterations_method = Iterations(matrix, epsilon)
        if self.power_up:
            eigenvalue, eigenvector, iterations = iterations_method.power_iteration_method()
            self.textBrowser.setText(f"Наибольшее собственное число (Прямой итерации): {eigenvalue}\n"
                                     f"Собственный вектор (Прямой итерации): {eigenvector}\n"
                                     f"Количество итераций (Прямой итерации): {iterations}")
        elif self.jakobi_up:
            eigenvalues, eigenvectors, iterations = iterations_method.jakobi_method()
            self.textBrowser.setText(f"Собственные числа (Вращения): {eigenvalues}\n"
                                     f'Матрица собственных векторов (Вращения): {eigenvectors}\n'
                                     f"кол-во итераций: {iterations}")
        else:
            self.textBrowser.setText("Метод не выбран")

    def jakobi_r(self):
        self.power_up = False
        self.jakobi_up = True

    def power_r(self):
        self.power_up = True
        self.jakobi_up = False

def main():
    row: int = int(input("Введите n для матрицы nxn "))
    col: int = row
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App(rows=row, cols=col)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()