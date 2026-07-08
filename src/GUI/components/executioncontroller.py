from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.components.error_box import ErrorBox
import math
import time

class ExecutionController():
    def __init__(self, gui, emulator):
        self.gui = gui
        self.emulator = emulator
        self.ram_view = gui.ram_view
        self.speed_control = gui.speed_control
        self.run_button = gui.ui.run_button
        self.step_button = gui.ui.step_button
        self.screen = gui.screen
        self.registers = gui.registers

        self.runtime_timer = QtCore.QTimer()
        self.runtime_timer.timeout.connect(self.run_batch)

        self.run_button.clicked.connect(self.toggle_run)
        self.step_button.clicked.connect(self.step_code)

        gui.ui.actionRun.triggered.connect(self.run_code)
        gui.ui.actionStop.triggered.connect(self.stop_code)
        gui.ui.actionStep.triggered.connect(self.step_code)

        self.time_since_last_batch = None
        self.running = False
        self.update_batch_size()

        gui.ui.speed_slider.actionTriggered.connect(self.update_batch_size)

        


    def run_batch(self):
        RAM_changes = []
        self.A_previous = self.emulator.A_value
        self.P_previous = self.emulator.P_value
        self.PC_previous = self.emulator.PC_value

        self.stopping = False
        
        for i in range(self.batch_size):
            try:
                RAM_change = self.emulator.execute_next_command()
                if RAM_change != None and RAM_change not in RAM_changes:
                    RAM_changes.append(RAM_change)
            except ValueError as e:
                self.stopping = True
                ErrorBox(str(e))
                break
            if self.ram_view.is_breakpoint(self.emulator.PC_value):
                self.stopping = True
                break
                   
        for change in RAM_changes:
            self.ram_view.update_RAM(change)

            self.screen.update_value(change)

        self.ram_view.update_RAM(self.A_previous)
        self.ram_view.update_RAM(self.P_previous)
        self.ram_view.update_RAM(self.PC_previous)

        self.ram_view.update_RAM(self.emulator.A_value)
        self.ram_view.update_RAM(self.emulator.P_value)
        self.ram_view.update_RAM(self.emulator.PC_value)

        self.registers.update()
        self.ram_view.scroll_to_item()

        if self.time_since_last_batch != None:
            self.speed_control.update_label(self.batch_size/(time.time()-self.time_since_last_batch))

        self.time_since_last_batch=time.time()

        if self.stopping:
            self.stop_code()

    def update_RAM(self, change):
        self.ram_view.update_RAM(change)

    def step_code(self):
        self.A_previous = self.emulator.A_value
        self.P_previous = self.emulator.P_value
        self.PC_previous = self.emulator.PC_value
        RAM_change = None
        try:
            RAM_change = self.emulator.execute_next_command()
        except ValueError as e:
            if self.emulator.PC_value != self.emulator.memory_size:
                ErrorBox(str(e))
        if RAM_change != None:
            self.ram_view.update_RAM(RAM_change)
            self.screen.update_value(RAM_change)

        self.ram_view.update_RAM(self.A_previous)
        self.ram_view.update_RAM(self.P_previous)
        self.ram_view.update_RAM(self.PC_previous)

        self.ram_view.update_RAM(self.emulator.A_value)
        self.ram_view.update_RAM(self.emulator.P_value)
        self.ram_view.update_RAM(self.emulator.PC_value)

        self.registers.update()

    def toggle_run(self):
        if not self.running:
            self.run_code()
        else:
            self.stop_code()

    def run_code(self):
        self.run_button.setText("Stop")
        self.runtime_timer.start()
        self.running = True
        for i in range(self.emulator.memory_size):
            self.ram_view.widget.item(i,1).setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
        

    def stop_code(self):
        self.run_button.setText("Run")
        self.runtime_timer.stop()
        self.running = False
        #self.ram_view.update_all_RAM()
        #self.screen.update_screen()
        #self.registers.update()
        for i in range(self.emulator.memory_size):
            self.ram_view.widget.item(i,1).setFlags(QtCore.Qt.ItemFlag.ItemIsEditable|QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)

    def update_batch_size(self):
        speed = self.speed_control.get_speed()

        self.batch_size = math.ceil(speed / 1000)
        self.runspeed = math.floor((1000 * self.batch_size) / speed)

        self.runtime_timer.setInterval(self.runspeed)



