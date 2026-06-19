import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.windowui import Ui_EmulatorWindow

from src.assembler import Assembler
from src.emulator import HackEmulator
from src.assembler_tools.tokentype import TokenType

class HACK_GUI():
    

    def __init__(self):
        
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_EmulatorWindow()

        self.ui.setupUi(self.window)

        Screen = QtWidgets.QGraphicsScene()
        self.ui.Screen_view.setScene(Screen)

        self.ui.actionLoad.triggered.connect(self.load_file)

    def open_window(self):
        self.window.show()

        sys.exit(self.app.exec())

    def load_file(self):

        file_name = QtWidgets.QFileDialog.getOpenFileName()[0]
        
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()

        for i in range(len(lines)):

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable|QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.ui.Code_view.setItem(i, 0, item)
            item.setText(lines[i].replace("\n",""))
        