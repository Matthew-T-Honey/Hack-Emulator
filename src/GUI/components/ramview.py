from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.components.speedcontrol import SpeedControl


class RamView():
    def __init__(self, gui, emulator):
        self.gui = gui
        self.widget = gui.ui.RAM_view
        self.run_button = gui.ui.run_button
        self.reset_button = gui.ui.reset_button
        self.emulator = emulator

        self.speed_control = SpeedControl(gui, self)

        for i in range(self.emulator.memory_size):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.widget.setItem(i, 0, item)
            item.setText(str(i))

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable|QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.widget.setItem(i, 1, item)

        self.update_all_RAM()
        self.widget.resizeColumnsToContents()

        self.run_button.clicked.connect(self.toggle_run)

        self.gui.ui.action_toggle_ram_view.triggered.connect(self.toggle_visible)

        self.running = False

        self.widget.itemClicked.connect(self.track_item)
        self.tracking = None


    def track_item(self, item):
        if item.row() == self.emulator.PC_value:
            self.tracking = "PC"
        elif item.row() == self.emulator.A_value:
            self.tracking = "A"
        elif item.row() == self.emulator.P_value:
            self.tracking = "P"
        else:
            self.tracking = None
        self.scroll_to_item()

    def scroll_to_item(self):
        scrollto = None

        if self.tracking == "A":
            scrollto = self.emulator.A_value
        if self.tracking == "PC":
            scrollto = self.emulator.PC_value
        if self.tracking == "P":
            scrollto = self.emulator.P_value
        if scrollto != None and scrollto >=0 and scrollto < self.emulator.memory_size:
            self.widget.scrollToItem(self.widget.item(scrollto, 0),QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)

    def update_all_RAM(self):
        for i in range(self.emulator.memory_size):
            self.update_RAM(i)
        self.A_previous = self.emulator.A_value
        self.P_previous = self.emulator.P_value
        self.PC_previous = self.emulator.PC_value


    def update_RAM(self,i):
        if i < 0 or i > self.emulator.memory_size:
            return
        if i in [self.emulator.A_value, self.emulator.P_value, self.emulator.PC_value]:
            color = QtGui.QColor(255,255,100)
        else:
            color = QtGui.QColor(255,255,255)
        ram_str_addition = ""
        address_str_addition = ""
        if i == self.emulator.A_value:
            address_str_addition += " (A)"
            ram_str_addition += " (M)"
        if i == self.emulator.P_value:
            address_str_addition += " (P)"
            ram_str_addition += " (S)"
        if i == self.emulator.PC_value:
            address_str_addition += " (PC)"

        self.widget.item(i, 0).setBackground(color)
        self.widget.item(i, 1).setBackground(color)
        self.widget.item(i, 0).setText(str(i) + address_str_addition)
        self.widget.item(i, 1).setText(format(self.emulator.get_value(i) % 2**16,'016b') + ram_str_addition)


    def toggle_run(self):
        if not self.running:
            self.run_code()
        else:
            self.stop_code()

    def run_code(self):
        self.run_button.setText("Stop")
        self.speed_control.runtime_timer.start()
        self.running = True

    def stop_code(self):
        self.run_button.setText("Run")
        self.speed_control.runtime_timer.stop()
        self.running = False
        
            
    def execute_next(self):
        
        self.emulator.execute_next_command()
        self.gui.update_registers()

        self.update_RAM(self.A_previous)
        self.update_RAM(self.P_previous)
        self.update_RAM(self.PC_previous)

        self.A_previous = self.emulator.A_value
        self.P_previous = self.emulator.P_value
        self.PC_previous = self.emulator.PC_value

        self.update_RAM(self.emulator.A_value)
        self.update_RAM(self.emulator.P_value)
        self.update_RAM(self.emulator.P_value + 1)
        self.update_RAM(self.emulator.PC_value)

        self.gui.screen.update_value(self.emulator.A_value)
        self.scroll_to_item()
        
    
    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.speed_control.widget.setVisible(self.widget.isVisible())
        self.run_button.setVisible(self.widget.isVisible())
        self.reset_button.setVisible(self.widget.isVisible())
    

