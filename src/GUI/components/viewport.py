from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.components.ramview import RamView


class Vieport(RamView):
    def __init__(self, gui, emulator):
        super().__init__(gui, emulator)







class Viewporrt():
    def __init__(self, gui, num):
        self.gui = gui
        if num == 1:
            self.widget = gui.ui.Viewport1
            self.register = "PC"
            self.format_dropdown = gui.ui.viewport_format_dropdown_1
        if num == 2:
            self.widget = gui.ui.Viewport2
            self.register = "A"
            self.format_dropdown = gui.ui.viewport_format_dropdown_2
        if num == 3:
            self.widget = gui.ui.Viewport3
            self.register = "P"
            self.format_dropdown = gui.ui.viewport_format_dropdown_3

        for i in range(self.emulator.memory_size):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.widget.setItem(i, 0, item)
            item.setText(str(i))

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable|QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.widget.setItem(i, 1, item)