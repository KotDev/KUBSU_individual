import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel


class Decoder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Decoder')
        self.resize(400, 200)


        input_layout = QHBoxLayout()
        output_layout = QVBoxLayout()


        self.inputs = []
        for i in range(3):
            button = QPushButton(f'Вход {i}')
            button.setCheckable(True)
            button.clicked.connect(self.updateOutputs)
            input_layout.addWidget(button)
            self.inputs.append(button)


        self.outputs = []
        for i in range(8):
            label = QLabel(f'- {i}: 0')
            output_layout.addWidget(label)
            self.outputs.append(label)


        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)


        self.setLayout(main_layout)

    def updateOutputs(self):
        input_values = [int(button.isChecked()) for button in self.inputs]
        input_number = input_values[0] + (input_values[1] << 1) + (input_values[2] << 2)

        for i, label in enumerate(self.outputs):
            label.setText(f'- {i}: {"1" if i == input_number else "0"}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    decoder = Decoder()
    decoder.show()
    sys.exit(app.exec_())