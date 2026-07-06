from PyQt6 import QtCore, QtGui, QtWidgets

class CodeView():
    def __init__(self, gui):
        self.widget = gui.ui.code_view
        self.token_view = gui.token_view
        self.load_button = gui.ui.load_button
        self.save_button = gui.ui.save_button

        self.lex_assemble_button = gui.ui.lex_assemble_button
        self.lex_assemble_button.clicked.connect(self.lex_or_assemble_code)

        gui.ui.actionLoad.triggered.connect(self.load_file)
        self.load_button.clicked.connect(self.load_file)

        gui.ui.actionSave_File.triggered.connect(self.save_file)
        self.save_button.clicked.connect(self.save_file)

        gui.ui.actionCode_View.triggered.connect(self.toggle_visible)


    def load_file(self):

        filename = QtWidgets.QFileDialog.getOpenFileName(self.widget, "Load File","","(*.asm)")[0]
        if filename:
            try:
                file = open(filename, "r")
                lines = file.readlines()
                filelines = ("").join(lines)
                file.close()
                self.widget.setPlainText(filelines)
            except:
                return

    def save_file(self):
        content = self.widget.toPlainText()
        filename = QtWidgets.QFileDialog.getSaveFileName(self.widget, "Save File","","(*.asm)")[0]
        if filename:
            f = open(filename,"w")
            f.write(content)
            f.close()


    def save_code_to_file(self,file):
        lines = self.widget.toPlainText()
        file.write(lines)

    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.lex_assemble_button.setVisible(self.widget.isVisible())
        self.save_button.setVisible(self.widget.isVisible())
        self.load_button.setVisible(self.widget.isVisible())

    def lex_or_assemble_code(self):
        if self.token_view.lex_code():
            if not self.token_view.widget.isVisible():
                self.token_view.parse_code()

    def get_code(self):
        return self.widget.toPlainText()


    