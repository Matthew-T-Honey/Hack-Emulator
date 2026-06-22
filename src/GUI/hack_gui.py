import sys
import time
from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.windowui import Ui_EmulatorWindow

from src.assembler import Assembler
from src.emulator import HackEmulator
from src.assembler_tools.tokentype import TokenType
from src.assembler_tools.lexer import Lexer
from src.assembler_tools.parser import Parser




class HACK_GUI():

    runspeed = 100
    

    def __init__(self):

        self.emulator = HackEmulator()

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_EmulatorWindow()

        self.ui.setupUi(self.window)

        #Screen = QtWidgets.QGraphicsScene()
        #self.ui.Screen_view.setScene(Screen)

        self.ui.actionLoad.triggered.connect(self.load_file)

        self.ui.lex_button.clicked.connect(self.lex_code)
        self.ui.parse_button.clicked.connect(self.parse_code)
        self.ui.run_button.clicked.connect(self.run_code)

        for i in range(self.emulator.memory_size):
            for j in range(6):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.ui.Token_view.setItem(i, j, item)

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.ui.RAM_view.setItem(i, 0, item)
            item.setText(str(i))

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable|QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.ui.RAM_view.setItem(i, 1, item)



        self.lexer = None
        self.lexer_tokens = None

        self.reset_token_view()
        self.update_RAM()
        self.update_registers()
        
        self.ui.RAM_view.resizeColumnsToContents()
        self.ui.RAM_view.horizontalHeader().setStretchLastSection(True)
        self.ui.Token_view.horizontalHeader().setStretchLastSection(True)

        self.runtime_timer = QtCore.QTimer()
        self.runtime_timer.setInterval(self.runspeed)
        self.runtime_timer.timeout.connect(self.execute_next)




    def open_window(self):
        self.window.show()

        sys.exit(self.app.exec())

    def load_file(self):

        file_name = QtWidgets.QFileDialog.getOpenFileName()[0]
        
        file = open(file_name, "r")
        lines = file.readlines()
        filelines = ("").join(lines)
        file.close()

        self.ui.Code_view.setText(filelines)
        

    def save_code_to_file(self,file):
        lines = self.ui.Code_view.toPlainText()
        file.write(lines)


    def lex_code(self):
        code_file = open("src/GUI/codefile.txt","w")
        self.save_code_to_file(code_file)
        code_file.close()

        self.lexer = Lexer()

        code_file = open("src/GUI/codefile.txt","r")
        self.lexer_tokens = self.lexer.lex_file(code_file)
        code_file.close()

        self.reset_token_view()
        self.set_token_view()


    def parse_code(self):
        if self.lexer == None or self.lexer_tokens == None:
            return
        
        parser = Parser()
        parser.parse_tokens(self.emulator,self.lexer_tokens,self.lexer.symbol_table)

        self.update_RAM()


    def update_RAM(self):
        for i in range(self.emulator.memory_size):
            self.ui.RAM_view.item(i, 1).setText(format(self.emulator.get_value(i) % 2**16,'016b'))

    def update_registers(self):
        self.ui.register_view.item(0, 0).setText(format(self.emulator.PC_value % 2**16,'016b'))
        self.ui.register_view.item(1, 0).setText(format(self.emulator.D_value % 2**16,'016b'))
        self.ui.register_view.item(2, 0).setText(format(self.emulator.A_value % 2**16,'016b'))
        self.ui.register_view.item(3, 0).setText(format(self.emulator.M_value % 2**16,'016b'))
        self.ui.register_view.item(4, 0).setText(format(self.emulator.P_value % 2**16,'016b'))
        self.ui.register_view.item(5, 0).setText(format(self.emulator.S_value % 2**16,'016b'))

    def set_token_view(self):
        for i in range(len(self.lexer_tokens)):
            for j in range(len(self.lexer_tokens[i])):
                if self.lexer_tokens[i][j].type == TokenType.DESTINATION:
                    col = 4
                elif self.lexer_tokens[i][j].type == TokenType.JUMP:
                    col = 5
                else:
                    col = j + 2
                self.ui.Token_view.item(i, col).setText(str(self.lexer_tokens[i][j].text))

        for symbol in self.lexer.symbol_table:
            self.ui.Token_view.item(self.lexer.symbol_table[symbol], 0).setText(symbol+":")

        self.ui.Token_view.resizeColumnsToContents()
        self.ui.Token_view.horizontalHeader().setStretchLastSection(True)

    def reset_token_view(self):
        for i in range(self.emulator.memory_size):
            for j in range(6):
                if j==1:
                    self.ui.Token_view.item(i,j).setText(str(i))
                else:
                    self.ui.Token_view.item(i,j).setText("")


    def run_code(self):
        self.runtime_timer.start()
            

    def execute_next(self):
        self.emulator.execute_next_command()
        self.update_registers()
        self.update_RAM()





