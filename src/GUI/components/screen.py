from PyQt6 import QtCore, QtGui, QtWidgets

class Screen():
    def __init__(self, gui, emulator):
        self.emulator = emulator
        self.screen = QtWidgets.QGraphicsScene()
        self.widget = gui.ui.screen_view
        self.size_button = gui.ui.screen_size_button

        self.scale = 1

        self.widget.setScene(self.screen)
        self.image = QtGui.QImage(512,256, QtGui.QImage.Format.Format_Mono)
        pixmap = QtGui.QPixmap.fromImage(self.image)
        self.pixmapitem = self.screen.addPixmap(pixmap)

        self.update_screen()

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.setInterval(10)
        self.update_timer.start()

        gui.ui.actionScreen_View.triggered.connect(self.toggle_visible)

        self.size_button.clicked.connect(self.update_size)

        self.border = 4
        self.widget.setFixedSize(512 + self.border,256 + self.border)


    def update_size(self):
        if self.scale == 1:
            self.scale = 2
            self.size_button.setText("Small Screen")
            self.widget.setFixedSize(1024 + self.border,512 + self.border)
            self.widget.scale(2,2)
        else:
            self.scale = 1
            self.size_button.setText("Large Screen")
            self.widget.setFixedSize(512 + self.border,256 + self.border)
            self.widget.scale(0.5,0.5)
        self.update_screen()


    def update_screen(self):
        for y in range(256):
            for x in range(32):
                val = self.emulator.get_value(16384 + y*32 + x)
                for i in range(16):
                    if (2**i & val) != 0:
                        self.image.setPixel(x*16 + i,y,0)
                    else:
                        self.image.setPixel(x*16 + i,y,1)
        self.update_display()

    def update_value(self, address):
        if address < 16384 or address >= 24576:
            return
        val = self.emulator.get_value(address)
        address -= 16384
        y = address // 32
        x = address % 32

        for i in range(16):
            if (2**i & val) != 0:
                self.image.setPixel(x*16 + i,y,0)
            else:
                self.image.setPixel(x*16 + i,y,1)


    def update_display(self):
        pixmap = QtGui.QPixmap.fromImage(self.image)
        self.pixmapitem.setPixmap(pixmap)

    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.size_button.setVisible(self.widget.isVisible())
        

