from PyQt6 import QtCore, QtGui, QtWidgets

class ErrorBox(QtWidgets.QDialog):
    def __init__(self, error_msg):
        super().__init__()
        self.setWindowTitle("Emulator Error")
        self.resize(200, 50)
        layout = QtWidgets.QVBoxLayout(self)
        error_message = QtWidgets.QLabel(error_msg)
        layout.addWidget(error_message)
        self.setLayout(layout)
        self.exec()



        