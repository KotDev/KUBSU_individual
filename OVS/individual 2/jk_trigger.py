import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QHBoxLayout

class JKFlipFlop:
    def __init__(self):
        self.Q = 0  # Output Q
        self.not_Q = 1  # Output not Q

    def update(self, J, K, clk):
        if clk:
            if J == 0 and K == 0:
                pass  # No change
            elif J == 0 and K == 1:
                self.Q = 0
            elif J == 1 and K == 0:
                self.Q = 1
            elif J == 1 and K == 1:
                self.Q = 1 - self.Q
            self.not_Q = 1 - self.Q

class JKFlipFlopGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.jk_flip_flop = JKFlipFlop()

        self.setWindowTitle("JK")
        self.setGeometry(100, 100, 300, 200)

        self.J = 0
        self.K = 0
        self.clk = 0

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # J inputs
        J_layout = QHBoxLayout()
        J_label = QLabel("J:")
        self.J_group = QButtonGroup(self)
        self.J0 = QRadioButton("0")
        self.J1 = QRadioButton("1")
        self.J0.setChecked(True)
        self.J_group.addButton(self.J0, 0)
        self.J_group.addButton(self.J1, 1)
        self.J_group.buttonClicked.connect(self.update_J)

        J_layout.addWidget(J_label)
        J_layout.addWidget(self.J0)
        J_layout.addWidget(self.J1)

        # K inputs
        K_layout = QHBoxLayout()
        K_label = QLabel("K:")
        self.K_group = QButtonGroup(self)
        self.K0 = QRadioButton("0")
        self.K1 = QRadioButton("1")
        self.K0.setChecked(True)
        self.K_group.addButton(self.K0, 0)
        self.K_group.addButton(self.K1, 1)
        self.K_group.buttonClicked.connect(self.update_K)

        K_layout.addWidget(K_label)
        K_layout.addWidget(self.K0)
        K_layout.addWidget(self.K1)

        # Clock inputs
        clk_layout = QHBoxLayout()
        clk_label = QLabel("C:")
        self.clk_group = QButtonGroup(self)
        self.clk0 = QRadioButton("0")
        self.clk1 = QRadioButton("1")
        self.clk0.setChecked(True)
        self.clk_group.addButton(self.clk0, 0)
        self.clk_group.addButton(self.clk1, 1)
        self.clk_group.buttonClicked.connect(self.update_clk)

        clk_layout.addWidget(clk_label)
        clk_layout.addWidget(self.clk0)
        clk_layout.addWidget(self.clk1)

        # Outputs
        self.Q_label = QLabel("Q: 0")
        self.not_Q_label = QLabel("not Q: 1")


        layout.addLayout(J_layout)
        layout.addLayout(K_layout)
        layout.addLayout(clk_layout)
        layout.addWidget(self.Q_label)
        layout.addWidget(self.not_Q_label)

        self.setLayout(layout)
        self.update_outputs()

    def update_J(self):
        self.J = self.J_group.checkedId()
        self.update_flip_flop()

    def update_K(self):
        self.K = self.K_group.checkedId()
        self.update_flip_flop()

    def update_clk(self):
        self.clk = self.clk_group.checkedId()
        self.update_flip_flop()

    def update_flip_flop(self):
        self.jk_flip_flop.update(self.J, self.K, self.clk)
        self.update_outputs()

    def update_outputs(self):
        self.Q_label.setText(f"Q1: {self.jk_flip_flop.Q}")
        self.not_Q_label.setText(f"Q2: {self.jk_flip_flop.not_Q}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = JKFlipFlopGUI()
    gui.show()
    sys.exit(app.exec_())