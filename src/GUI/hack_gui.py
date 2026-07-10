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
from src.GUI.components.speedcontrol import SpeedControl
from src.GUI.components.keyboard import Keyboard
from src.GUI.components.registers import Registers
from src.GUI.components.executioncontroller import ExecutionController

class HACK_GUI():

    def __init__(self):


        self.emulator = HackEmulator()

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow(self)
        self.ui = Ui_EmulatorWindow()

        self.ui.setupUi(self.window)

        self.token_view = TokenView(self, self.emulator)
        self.code_view = CodeView(self)
        self.speed_control = SpeedControl(self)
        self.registers = Registers(self, self.emulator)
        self.screen = Screen(self, self.emulator)
        self.ram_view = RamView(self, self.emulator)
        
        self.keyboard = Keyboard(self, self.emulator)

        self.ram_view.keyboard = self.keyboard
        self.token_view.ram_view = self.ram_view
        self.registers.ram_view = self.ram_view
        self.registers.update()
        self.token_view.widget.verticalScrollBar().valueChanged.connect(self.ram_view.update_scrollbar)
        

        self.execution_controller = ExecutionController(self, self.emulator)
    
        self.ui.reset_button.clicked.connect(self.reset_emulator)
        self.ui.actionReset.triggered.connect(self.reset_emulator)
        self.ram_view.update_all_RAM()

        QtWidgets.QApplication.instance().installEventFilter(self.window)

    def open_window(self):
        self.window.show()

        sys.exit(self.app.exec())

    def reset_emulator(self):
        self.execution_controller.stop_code()
        self.token_view.parse_code()

    
    
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, gui):
        self.gui = gui
        super().__init__()

    def eventFilter(self, widget, event):
        if widget.objectName() == "EmulatorWindowWindow":
            if event.type() == QtCore.QEvent.Type.KeyPress:
                if not event.isAutoRepeat():
                    self.gui.keyboard.key_pressed(event)
            if event.type() == QtCore.QEvent.Type.KeyRelease:
                if not event.isAutoRepeat():
                    self.gui.keyboard.key_released(event)
        if event.type() == QtCore.QEvent.Type.Wheel:
            self.gui.ram_view.tracking = None
        return False





