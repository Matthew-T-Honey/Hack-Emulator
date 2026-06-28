import sys
import time
import math
from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.windowui import Ui_EmulatorWindow

from src.assembler import Assembler
from src.emulator import HackEmulator

from src.assembler_tools.parser import Parser
from src.GUI.components.screen import Screen
from src.GUI.components.codeview import CodeView
from src.GUI.components.tokenview import TokenView
from src.GUI.components.ramview import RamView




class HACK_GUI():


    def __init__(self):


        self.emulator = HackEmulator()

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_EmulatorWindow()

        self.ui.setupUi(self.window)

        self.token_view = TokenView(self, self.emulator)
        self.code_view = CodeView(self)
        
        self.ram_view = RamView(self, self.emulator)
        self.screen = Screen(self, self.emulator)
        
        self.update_registers()

        self.ui.reset_button.clicked.connect(self.reset_emulator)

    def open_window(self):
        self.window.show()

        sys.exit(self.app.exec())

    def update_registers(self):
        self.ui.register_view.item(0, 0).setText(format(self.emulator.PC_value % 2**16,'016b'))
        self.ui.register_view.item(1, 0).setText(format(self.emulator.D_value % 2**16,'016b'))
        self.ui.register_view.item(2, 0).setText(format(self.emulator.A_value % 2**16,'016b'))
        self.ui.register_view.item(3, 0).setText(format(self.emulator.M_value % 2**16,'016b'))
        self.ui.register_view.item(4, 0).setText(format(self.emulator.P_value % 2**16,'016b'))
        self.ui.register_view.item(5, 0).setText(format(self.emulator.S_value % 2**16,'016b'))

    def reset_emulator(self):
        self.ram_view.stop_code()
        self.emulator.reset()
        self.update_registers()
        self.ram_view.update_all_RAM()
        
    






