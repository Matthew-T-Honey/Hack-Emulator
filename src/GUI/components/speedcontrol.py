from PyQt6 import QtCore, QtGui, QtWidgets
import math
from collections import deque

class SpeedControl():
    def __init__(self, gui):
        self.gui = gui
        self.speed_slider = gui.ui.speed_slider
        self.speed_label = gui.ui.speed_label
        self.target_label = gui.ui.target_label
        
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
            if average_time >= 100:
                self.speed_label.setText("Speed: "+str(int(average_time)))
            else:
                self.speed_label.setText("Speed: "+str(round(average_time,2)))
            

    def reset_label(self):
        self.speed_label.setText("Speed: 0")
        self.times = deque()
        
    def update_speed(self):
        if self.speed_slider.value()<10:
            self.speed = 10**((self.speed_slider.value()/10)-1)
        else:
            self.speed = 10**((self.speed_slider.value()/5)-2)
        self.speed_label.setText("Speed: 0")
        if self.speed >= 100:
            self.target_label.setText("Target: "+str(int(self.speed)))
        else:
            self.target_label.setText("Target: "+str(round(self.speed,2)))
        self.times = deque()
