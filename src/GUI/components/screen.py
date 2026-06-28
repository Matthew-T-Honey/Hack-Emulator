from PyQt6 import QtCore, QtGui, QtWidgets

class Screen():
    def __init__(self, gui, emulator):
        self.emulator = emulator
        self.screen = QtWidgets.QGraphicsScene()
        self.widget = gui.ui.screen_view

        self.widget.setScene(self.screen)
        self.image = QtGui.QImage(512,256, QtGui.QImage.Format.Format_Mono)
        pixmap = QtGui.QPixmap.fromImage(self.image)
        self.pixmapitem = self.screen.addPixmap(pixmap)

        self.update_screen()

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.setInterval(10)
        self.update_timer.start()

        gui.ui.action_toggle_screen_view.triggered.connect(self.toggle_visible)



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
        

