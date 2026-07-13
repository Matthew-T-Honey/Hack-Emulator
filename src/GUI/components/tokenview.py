from PyQt6 import QtCore, QtGui, QtWidgets
from src.assembler_tools.tokentype import TokenType
from src.assembler_tools.lexer import Lexer
from src.assembler_tools.parser import Parser
from src.GUI.components.error_box import ErrorBox

class TokenView():
    def __init__(self, gui, emulator):
        self.gui = gui
        self.emulator = emulator
        self.widget = gui.ui.token_view
        self.lexer_tokens = None
        self.lexer = None


        self.lex_assemble_button = gui.ui.lex_assemble_button
        self.parse_button = gui.ui.parse_button

        for i in range(self.emulator.memory_size):
            for j in range(6):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.widget.setItem(i, j, item)

        self.parse_button.clicked.connect(self.parse_code)

        self.reset_token_view()

        gui.ui.actionToken_View.triggered.connect(self.toggle_visible)
        gui.ui.actionLex_Code.triggered.connect(self.lex_code)
        gui.ui.actionParse_Tokens.triggered.connect(self.parse_code)
        gui.ui.actionAssemble_Code.triggered.connect(self.assemble_code)

        self.widget.resizeColumnsToContents()

        
    def assemble_code(self):
        if self.lex_code():
            self.parse_code()

    def update_scrollbar(self, value):
        if value != self.widget.verticalScrollBar().value():
            self.widget.verticalScrollBar().setValue(value)


    def set_token_view(self):
        for i in range(len(self.lexer_tokens)):
            for j in range(len(self.lexer_tokens[i])):
                if self.lexer_tokens[i][j].type == TokenType.DESTINATION:
                    col = 4
                elif self.lexer_tokens[i][j].type == TokenType.JUMP:
                    col = 5
                else:
                    col = j + 2
                self.widget.item(i, col).setText(str(self.lexer_tokens[i][j].text))

        for symbol in self.lexer.symbol_table:
            self.widget.item(self.lexer.symbol_table[symbol], 0).setText(symbol+":")

        self.widget.resizeColumnsToContents()

    def reset_token_view(self):
        for i in range(self.emulator.memory_size):
            for j in range(6):
                if j==1:
                    self.widget.item(i,j).setText(str(i))
                else:
                    self.widget.item(i,j).setText("")

        
        self.widget.resizeColumnsToContents()


    def lex_code(self):
        code = self.gui.code_view.get_code()

        self.lexer = Lexer()
        try:
            self.lexer_tokens = self.lexer.lex_string(code)
        except SyntaxError as e:
            self.lexer_tokens = None
            ErrorBox(str(e))
            return False

        self.reset_token_view()
        self.set_token_view()

        return True

    def parse_code(self):
        self.execution_controller.stop_code()
        self.emulator.reset()

        if self.lexer == None or self.lexer_tokens == None:
            self.gui.ram_view.update_all_RAM()
            return

        parser = Parser()
        try:
            parser.parse_tokens(self.emulator,self.lexer_tokens,self.lexer.symbol_table)
        except SyntaxError as e:
            self.emulator.reset()
            ErrorBox(str(e))
            return False

        self.gui.ram_view.update_all_RAM()
        
        return True

    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.parse_button.setVisible(self.widget.isVisible())
        if self.widget.isVisible():
            self.lex_assemble_button.setText("Lex")
        else:
            self.lex_assemble_button.setText("Assemble")


    