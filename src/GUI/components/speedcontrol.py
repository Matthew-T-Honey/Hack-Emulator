from PyQt6 import QtCore, QtGui, QtWidgets
import time

class SpeedControl():
    def __init__(self, gui, ram_view):
        self.widget = gui.ui.speed_widget
        self.speed_slider = gui.ui.speed_slider
        self.speed_label = gui.ui.speed_label
        self.ram_view = ram_view
        self.t_list = []
        self.t = None

        self.runtime_timer = QtCore.QTimer()
        self.runtime_timer.timeout.connect(self.run_iteration)

        self.update_speed()

        self.speed_slider.actionTriggered.connect(self.update_speed)
        

    def update_speed(self):
        self.runspeed = 10**((self.speed_slider.value()/10))
        self.runtime_timer.setInterval(int(1000/self.runspeed))

        self.t = None
        self.t_list = []

    def run_iteration(self):
        if self.t != None:
            self.t_list.append(1/(time.time()-self.t))
            if len(self.t_list) > 1/(time.time()-self.t):
                self.t_list.pop(0)
        if len(self.t_list) > 0:
            self.speed_label.setText(str(round(sum(self.t_list)/len(self.t_list),2)))
        self.t=time.time()
        
        self.ram_view.execute_next()