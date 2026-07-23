from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.components.error_box import ErrorBox
import math
import time
import random

class ExecutionController():
    def __init__(self, gui, emulator):
        self.gui = gui
        self.emulator = emulator
        self.run_button = gui.ui.run_button
        self.step_button = gui.ui.step_button

        self.runtime_timer = QtCore.QTimer()
        self.runtime_timer.timeout.connect(self.run_batch)

        self.run_button.clicked.connect(self.toggle_run)
        self.step_button.clicked.connect(self.step_code)

        gui.ui.actionToggle_Run.triggered.connect(self.toggle_run)
        gui.ui.actionStep.triggered.connect(self.step_code)

        self.time_since_last_batch = None
        self.running = False
        self.update_batch_size()

        gui.ui.speed_slider.valueChanged.connect(self.update_batch_size)




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
            if self.gui.ram_view.is_breakpoint(self.emulator.PC_value):
                self.stopping = True
                self.gui.ram_view.go_to_item(self.emulator.PC_value)
                break
                   
        for change in RAM_changes:
            self.gui.ram_view.update_RAM(change)

        self.gui.ram_view.update_RAM(self.A_previous)
        self.gui.ram_view.update_RAM(self.P_previous)
        self.gui.ram_view.update_RAM(self.PC_previous)

        self.gui.ram_view.update_RAM(self.emulator.A_value)
        self.gui.ram_view.update_RAM(self.emulator.P_value)
        self.gui.ram_view.update_RAM(self.emulator.PC_value)

        self.gui.registers.update()
        self.gui.ram_view.scroll_to_tracking()

        if self.time_since_last_batch != None:
            self.gui.speed_control.update_label(self.batch_size/(time.time()-self.time_since_last_batch))

        self.time_since_last_batch=time.time()

        if self.stopping:
            self.stop_code()

    def update_RAM(self, change):
        self.gui.ram_view.update_RAM(change)

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
            self.gui.ram_view.update_RAM(RAM_change)
            self.gui.screen.update_value(RAM_change)

        self.gui.ram_view.update_RAM(self.A_previous)
        self.gui.ram_view.update_RAM(self.P_previous)
        self.gui.ram_view.update_RAM(self.PC_previous)

        self.gui.ram_view.update_RAM(self.emulator.A_value)
        self.gui.ram_view.update_RAM(self.emulator.P_value)
        self.gui.ram_view.update_RAM(self.emulator.PC_value)

        self.gui.registers.update()

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
            self.gui.ram_view.widget.item(i,1).setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
        

    def stop_code(self):
        self.gui.speed_control.reset_label()
        self.run_button.setText("Run")
        self.runtime_timer.stop()
        self.running = False
        for i in range(self.emulator.memory_size):
            self.gui.ram_view.widget.item(i,1).setFlags(QtCore.Qt.ItemFlag.ItemIsEditable|QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)

    def update_batch_size(self):
        speed = self.gui.speed_control.get_speed()

        self.batch_size = math.ceil(speed / 1000)

        if self.batch_size >= 100:
            #Some randomness so that loopsize and batch size lining up doesn't look weird
            self.batch_size += random.randint(-5,5)

        self.runspeed = math.floor((1000 * self.batch_size) / speed)

        self.runtime_timer.setInterval(self.runspeed)

        



