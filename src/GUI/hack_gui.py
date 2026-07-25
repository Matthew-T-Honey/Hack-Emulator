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

        for action in [self.ui.actionCode_View,
                       self.ui.actionToken_View,
                       self.ui.actionRAM_View,
                       self.ui.actionRegister_View,
                       self.ui.actionScreen_View,
                       self.ui.actionKeyboard_View]:
            action.setChecked(True)


        self.token_view = TokenView(self, self.emulator)
        self.code_view = CodeView(self)
        self.speed_control = SpeedControl(self)
        self.registers = Registers(self, self.emulator)
        self.screen = Screen(self, self.emulator)
        self.ram_view = RamView(self, self.emulator)
        self.keyboard = Keyboard(self, self.emulator)
        self.execution_controller = ExecutionController(self, self.emulator)


        self.ram_view.update_all_RAM()
        self.ram_view.widget.resizeColumnsToContents()
        self.token_view.widget.verticalScrollBar().valueChanged.connect(self.ram_view.update_scrollbar)
        self.token_view.widget.verticalScrollBar().sliderPressed.connect(self.ram_view.stop_tracking)


        self.ui.reset_button.clicked.connect(self.reset_emulator)
        self.ui.actionReset.triggered.connect(self.reset_emulator)
        self.ram_view.update_all_RAM()

        QtWidgets.QApplication.instance().installEventFilter(self.window)

        if self.app.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Dark:
            self.ui.actionDark_Mode.setChecked(True)
        self.ui.actionDark_Mode.toggled.connect(self.toggle_dark_mode)

    def open_window(self):
        self.window.show()
        sys.exit(self.app.exec())

    def reset_emulator(self):
        self.token_view.parse_code()

    def toggle_dark_mode(self, toggled_on):
        if toggled_on == True:
            self.app.styleHints().setColorScheme(QtCore.Qt.ColorScheme.Dark)
        elif toggled_on == False:
            self.app.styleHints().setColorScheme(QtCore.Qt.ColorScheme.Light)
    
    
        
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
            if event.type() == QtCore.QEvent.Type.Close:
                return self.on_close(event)
        if event.type() == QtCore.QEvent.Type.Wheel:
            self.gui.ram_view.tracking = None
        
        return False
    
    def on_close(self, event):
        if self.gui.code_view.saved or (self.gui.code_view.widget.toPlainText() == "" and self.gui.code_view.codefile == None):
            event.accept()
            return False
        else:
            ret = QtWidgets.QMessageBox.question(self, "Exiting...",
                "You might have unsaved code,\nWould you like to save?",
                QtWidgets.QMessageBox.StandardButton.Save |
                QtWidgets.QMessageBox.StandardButton.Discard |
                QtWidgets.QMessageBox.StandardButton.Cancel)
            
            if ret == QtWidgets.QMessageBox.StandardButton.Save:
                self.gui.code_view.save_file()
            elif ret == QtWidgets.QMessageBox.StandardButton.Cancel:
                event.ignore()
                return True
            event.accept()
            return False




