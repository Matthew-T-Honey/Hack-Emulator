from PyQt6 import QtCore, QtGui, QtWidgets

class CodeView():
    def __init__(self, gui):
        self.gui = gui
        self.widget = gui.ui.code_view
        self.load_button = gui.ui.load_button
        self.save_button = gui.ui.save_button
        self.lex_assemble_button = gui.ui.lex_assemble_button
        self.line_numbers = gui.ui.code_line_numbers
        self.code_search = gui.ui.code_search
        self.filename_label = gui.ui.filename_label


        self.lex_assemble_button.clicked.connect(self.lex_or_assemble_code)

        gui.ui.actionLoad.triggered.connect(self.load_file)
        self.load_button.clicked.connect(self.load_file)

        gui.ui.actionSave_File.triggered.connect(self.save_file)
        self.save_button.clicked.connect(self.save_file)

        gui.ui.actionSave_As.triggered.connect(self.save_as_file)
        gui.ui.actionNew.triggered.connect(self.new_file)

        gui.ui.actionCode_View.triggered.connect(self.toggle_visible)

        self.set_num_of_lines()

        self.line_numbers.verticalScrollBar().valueChanged.connect(self.scroll_line_numbers)
        self.widget.verticalScrollBar().valueChanged.connect(self.scroll_code)

        self.widget.textChanged.connect(self.set_num_of_lines)
        self.code_search.textChanged.connect(self.search_code)
        self.code_search.returnPressed.connect(self.next_search)

        self.codefile = None
        self.saved = False
        self.widget.textChanged.connect(self.update_filename)


        pixmapi = QtWidgets.QStyle.StandardPixmap.SP_DialogOpenButton
        icon = self.gui.window.style().standardIcon(pixmapi)
        self.load_button.setIcon(icon)

        pixmapi = QtWidgets.QStyle.StandardPixmap.SP_DialogSaveButton
        icon = self.gui.window.style().standardIcon(pixmapi)
        self.save_button.setIcon(icon)

        pixmapi = QtWidgets.QStyle.StandardPixmap.SP_ArrowRight
        icon = self.gui.window.style().standardIcon(pixmapi)
        self.lex_assemble_button.setIcon(icon)



    def update_filename(self):
        if self.saved:
            self.filename_label.setText(self.codefile.split("/")[-1]+"*")
            self.saved = False

    def search_code(self):
        text = self.code_search.text()
        self.widget.setTextCursor(self.widget.document().find(text,0))

    def next_search(self):
        text = self.code_search.text()
        self.widget.setTextCursor(self.widget.document().find(text,self.widget.textCursor()))

    def set_num_of_lines(self):
        num = self.widget.toPlainText().count("\n")
        lines = ""
        for i in range(num+1):
            lines += str(i+1)+".\n"
        lines = lines[:-1]

        self.previous_scrollbar_position = self.line_numbers.verticalScrollBar().value()
        self.line_numbers.setPlainText(lines)
        self.line_numbers.verticalScrollBar().setValue(self.previous_scrollbar_position)

    def scroll_line_numbers(self, value):
        self.widget.verticalScrollBar().setValue(value)

    def scroll_code(self, value):
        self.line_numbers.verticalScrollBar().setValue(value)

    def new_file(self):
        if not self.saved and (self.widget.toPlainText() != "" or self.codefile != None):
            ret = QtWidgets.QMessageBox.question(self.gui.window, "Opening...",
            "You have unsaved code,\nWould you like to save?",
            QtWidgets.QMessageBox.StandardButton.Save |
            QtWidgets.QMessageBox.StandardButton.Discard |
            QtWidgets.QMessageBox.StandardButton.Cancel)

            if ret == QtWidgets.QMessageBox.StandardButton.Save:
                self.save_file()
            elif ret == QtWidgets.QMessageBox.StandardButton.Cancel:
                return
        self.codefile = None
        self.saved = False
        self.widget.setPlainText("")
        self.filename_label.setText("Untitled.asm*")


    def load_file(self):
        if not self.saved and (self.widget.toPlainText() != "" or self.codefile != None):
            ret = QtWidgets.QMessageBox.question(self.gui.window, "Opening...",
            "You have unsaved code,\nWould you like to save?",
            QtWidgets.QMessageBox.StandardButton.Save |
            QtWidgets.QMessageBox.StandardButton.Discard |
            QtWidgets.QMessageBox.StandardButton.Cancel)

            if ret == QtWidgets.QMessageBox.StandardButton.Save:
                self.save_file()
            elif ret == QtWidgets.QMessageBox.StandardButton.Cancel:
                return

        filename = QtWidgets.QFileDialog.getOpenFileName(self.widget, "Load File","","(*.asm)")[0]
        if filename:
            try:
                file = open(filename, "r")
                lines = file.readlines()
                filelines = ("").join(lines)
                file.close()
                self.widget.setPlainText(filelines)
                self.codefile = filename
                self.filename_label.setText(self.codefile.split("/")[-1])
                self.saved = True
            except:
                return

    def save_file(self):
        if self.codefile != None:
            content = self.widget.toPlainText()
            f = open(self.codefile,"w")
            f.write(content)
            f.close()
            self.saved = True
            self.filename_label.setText(self.codefile.split("/")[-1])
        else:
            self.save_as_file()


    def save_as_file(self):
        content = self.widget.toPlainText()
        filename = QtWidgets.QFileDialog.getSaveFileName(self.widget, "Save File","","(*.asm)")[0]
        if filename:
            f = open(filename,"w")
            f.write(content)
            f.close()
            self.codefile = filename
            self.filename_label.setText(self.codefile.split("/")[-1])
            self.saved = True


    def save_code_to_file(self,file):
        lines = self.widget.toPlainText()
        file.write(lines)

    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.lex_assemble_button.setVisible(self.widget.isVisible())
        self.save_button.setVisible(self.widget.isVisible())
        self.load_button.setVisible(self.widget.isVisible())
        self.line_numbers.setVisible(self.widget.isVisible())
        self.code_search.setVisible(self.widget.isVisible())
        self.filename_label.setVisible(self.widget.isVisible())

    def lex_or_assemble_code(self):
        if self.gui.token_view.lex_code():
            if not self.gui.token_view.widget.isVisible():
                self.gui.token_view.parse_code()

    def get_code(self):
        return self.widget.toPlainText()


    