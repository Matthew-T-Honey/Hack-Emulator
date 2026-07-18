from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.components.keymapping import KeyMapping

class Keyboard():
    kbd_address = 24576
    def __init__(self, gui, emualtor):
        self.gui = gui
        self.emulator = emualtor
        self.widget = gui.ui.KBD_view
        self.checkbox = gui.ui.KBD_checkbox

        self.held_keys = []
        self.checkbox.stateChanged.connect(self.update)
        gui.ui.actionKeyboard_View.triggered.connect(self.toggle_visible)


    def key_pressed(self, key):
        key_int = KeyMapping.keyevent_to_int(key)
        if key_int != 0 and key_int not in self.held_keys:
            self.held_keys.insert(0,key_int)
            self.update()

    def key_released(self, key):
        key_int = KeyMapping.keyevent_to_int(key)
        if key_int != 0 and key_int in self.held_keys:
            self.held_keys.remove(key_int)
            self.update()

    def update(self):
        if len(self.held_keys) == 0 or not self.checkbox.isChecked():
            self.widget.item(0,1).setText("")
            self.emulator.set_value(self.kbd_address, 0)
        else:
            self.widget.item(0,1).setText(KeyMapping.special_char_to_string(self.held_keys[0]))
            self.emulator.set_value(self.kbd_address, self.held_keys[0])
    
        if self.gui.ram_view.format == "Binary":
            val_string = format(self.emulator.get_value(self.kbd_address) % 2**16,'016b')
            val_string = val_string[:4]+" "+val_string[4:8]+" "+val_string[8:12]+" "+val_string[12:16]
        elif self.gui.ram_view.format == "Hexadecimal":
            val_string = format(self.emulator.get_value(self.kbd_address) % 2**16,'04X')
        elif self.gui.ram_view.format == "Decimal":
            val_string = str(self.emulator.get_value(self.kbd_address))
        elif self.gui.ram_view.format == "Assembly":
            val_string = format(self.emulator.get_value(self.kbd_address) % 2**16,'016b')
        else:
            raise SyntaxError("No format: "+self.format)
        self.widget.item(0,0).setText(val_string)
        self.gui.ram_view.update_RAM(self.kbd_address)

    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.checkbox.setVisible(self.widget.isVisible())
        

        