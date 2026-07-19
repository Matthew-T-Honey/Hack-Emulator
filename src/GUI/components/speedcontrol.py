from PyQt6 import QtCore, QtGui, QtWidgets
import time
from collections import deque

class SpeedControl():
    def __init__(self, gui):
        self.widget = gui.ui.speed_widget
        self.speed_slider = gui.ui.speed_slider
        self.speed_label = gui.ui.speed_label
        
        self.times = deque()
        self.speed = 1

        self.speed_slider.valueChanged.connect(self.update_speed)

    def get_speed(self):
        return self.speed
        
    
    def update_label(self,val):
        self.times.append(val)
        if len(self.times)>val + 1 or len(self.times) > 1000:
            self.times.popleft()
        if len(self.times)>0:
            average_time = sum(self.times)/len(self.times)
            self.speed_label.setText(str(round(average_time,2)))

    def reset_label(self):
        self.speed_label.setText("0")
        self.times = deque()
        
    def update_speed(self):
        if self.speed_slider.value()<10:
            self.speed = 10**((self.speed_slider.value()/10)-1)
        else:
            self.speed = 10**((self.speed_slider.value()/5)-2)
        print(self.speed)
        self.times = deque()
