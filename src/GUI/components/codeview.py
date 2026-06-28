from PyQt6 import QtCore, QtGui, QtWidgets

class CodeView():
    def __init__(self, gui):
        self.widget = gui.ui.code_view
        self.token_view = gui.token_view

        self.lex_assemble_button = gui.ui.lex_assemble_button
        self.lex_assemble_button.clicked.connect(self.lex_or_assemble_code)

        gui.ui.actionLoad.triggered.connect(self.load_file)

        gui.ui.action_toggle_code_view.triggered.connect(self.toggle_visible)

        

    def load_file(self):

        file_name = QtWidgets.QFileDialog.getOpenFileName()[0]
        try:
            file = open(file_name, "r")
            lines = file.readlines()
            filelines = ("").join(lines)
            file.close()
        except:
            print("no file found")

        self.widget.setText(filelines)

    def save_code_to_file(self,file):
        lines = self.widget.toPlainText()
        file.write(lines)

    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.lex_assemble_button.setVisible(self.widget.isVisible())

    def lex_or_assemble_code(self):
        self.token_view.lex_code()
        if not self.token_view.widget.isVisible():
            self.token_view.parse_code()


    