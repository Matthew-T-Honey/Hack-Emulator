from PyQt6 import QtCore, QtGui, QtWidgets
from src.assembler_tools.tokentype import TokenType
from src.assembler_tools.lexer import Lexer
from src.assembler_tools.parser import Parser

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

        self.widget.horizontalHeader().setStretchLastSection(True)
        self.widget.horizontalHeader().setCascadingSectionResizes(True)

        self.parse_button.clicked.connect(self.parse_code)

        self.reset_token_view()

        self.gui.ui.action_toggle_token_view.triggered.connect(self.toggle_visible)


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
        code_file = open("src/GUI/codefile.txt","w")
        self.gui.code_view.save_code_to_file(code_file)
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
        
        self.emulator.reset()

        parser = Parser()
        parser.parse_tokens(self.emulator,self.lexer_tokens,self.lexer.symbol_table)

        self.gui.ram_view.update_all_RAM()

    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.parse_button.setVisible(self.widget.isVisible())
        if self.widget.isVisible():
            self.lex_assemble_button.setText("Lex")
        else:
            self.lex_assemble_button.setText("Assemble")