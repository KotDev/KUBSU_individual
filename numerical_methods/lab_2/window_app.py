# -*- coding: utf-8 -*-
import sys

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from sympy import lambdify, symbols

from numerical_methods.lab_2.methods import Schedule


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(426, 336)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 180, 93, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_2.addWidget(self.lineEdit_3)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 240, 246, 26))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(10, 80, 211, 42))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.label = QtWidgets.QLabel(self.splitter_2)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit.setObjectName("lineEdit")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(10, 20, 371, 42))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.splitter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.layoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, 140, 92, 30))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(200, 140, 191, 91))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 426, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "b = "))
        self.pushButton_3.setText(_translate("MainWindow", "Левый"))
        self.pushButton_2.setText(_translate("MainWindow", "Средний"))
        self.pushButton.setText(_translate("MainWindow", "Правый"))
        self.label.setText(_translate("MainWindow", "Точность"))
        self.label_3.setText(_translate("MainWindow", "Функция"))
        self.label_2.setText(_translate("MainWindow", "a = "))


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    # Обработчики кнопок
    def on_pushButton_3_clicked(self):
        a = self.lineEdit_2.text()
        b = self.lineEdit_3.text()
        accuracy = self.lineEdit.text()
        function_str = self.lineEdit_4.text()
        if function_str:
            x = symbols("x")
            function = lambdify(x, function_str)

            if a and b and accuracy:
                self.textBrowser.clear()
                sh = Schedule(function, float(a), float(b), float(accuracy), method="left")
                sh.render()
                self.textBrowser.append(f"Интеграл: {sh.integral}")
                self.textBrowser.append(f"Разбиений: {sh.n}")
                self.textBrowser.append(f"Шаг: {sh.step}")
        self.clear_inputs()

    def on_pushButton_2_clicked(self):
        a = self.lineEdit_2.text()
        b = self.lineEdit_3.text()
        accuracy = self.lineEdit.text()
        function_str = self.lineEdit_4.text()
        if function_str:
            x = symbols("x")
            function = lambdify(x, function_str)

            if a and b and accuracy:
                self.textBrowser.clear()
                sh = Schedule(function, float(a), float(b), float(accuracy), method="mid")
                sh.render()
                self.textBrowser.append(f"Интеграл: {sh.integral}")
                self.textBrowser.append(f"Разбиений: {sh.n}")
                self.textBrowser.append(f"Шаг: {sh.step}")
        self.clear_inputs()

    def on_pushButton_clicked(self):
        a = self.lineEdit_2.text()
        b = self.lineEdit_3.text()
        accuracy = self.lineEdit.text()
        function_str = self.lineEdit_4.text()
        if function_str:
            x = symbols("x")
            function = lambdify(x, function_str)

            if a and b and accuracy:
                self.textBrowser.clear()
                sh = Schedule(function, float(a), float(b), float(accuracy), method="right")
                sh.render()
        self.clear_inputs()

    def clear_inputs(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()