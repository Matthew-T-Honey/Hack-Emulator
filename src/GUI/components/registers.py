

class Registers():
    def __init__(self, gui, emulator):
        self.PC_register = gui.ui.PC_register
        self.D_register = gui.ui.D_register
        self.A_register = gui.ui.A_register
        self.M_register = gui.ui.M_register
        self.P_register = gui.ui.P_register
        self.S_register = gui.ui.S_register
        self.emulator = emulator

        gui.ui.actionRegister_View.triggered.connect(self.toggle_visible)
        gui.ui.actionToggle_Stack_View.triggered.connect(self.toggle_stack_view)

        self.stack_view = True

        self.PC_register.itemClicked.connect(self.track_PC)
        self.A_register.itemClicked.connect(self.track_A)
        self.M_register.itemClicked.connect(self.track_A)
        self.P_register.itemClicked.connect(self.track_P)
        self.S_register.itemClicked.connect(self.track_P)

    def update(self):
        self.update_one(self.PC_register,self.emulator.PC_value)
        self.update_one(self.D_register,self.emulator.D_value)
        self.update_one(self.A_register,self.emulator.A_value)
        self.update_one(self.M_register,self.emulator.M_value)
        self.update_one(self.P_register,self.emulator.P_value)
        self.update_one(self.S_register,self.emulator.S_value)


    def update_one(self,register,value):
        if self.ram_view.format == "Binary":
            val_string = format(value % 2**16,'016b')
            val_string = val_string[:4]+" "+val_string[4:8]+" "+val_string[8:12]+" "+val_string[12:16]
        elif self.ram_view.format == "Hexadecimal":
            val_string = format(value % 2**16,'04X')
        elif self.ram_view.format == "Decimal":
            val_string = str(value)
        elif self.ram_view.format == "Assembly":
            val_string = format(value % 2**16,'016b')
            val_string = val_string[:4]+" "+val_string[4:8]+" "+val_string[8:12]+" "+val_string[12:16]
        else:
            raise SyntaxError("No format: "+self.ram_view.format)
        register.item(0,0).setText(val_string)

    def toggle_visible(self):
        self.PC_register.setVisible(not self.PC_register.isVisible())
        self.D_register.setVisible(not self.D_register.isVisible())
        self.A_register.setVisible(not self.A_register.isVisible())
        self.M_register.setVisible(not self.M_register.isVisible())
        self.P_register.setVisible(not self.P_register.isVisible() and self.stack_view)
        self.S_register.setVisible(not self.S_register.isVisible() and self.stack_view)
        
    def toggle_stack_view(self):
        self.stack_view = not self.stack_view
        self.P_register.setVisible(self.PC_register.isVisible() and self.stack_view)
        self.S_register.setVisible(self.PC_register.isVisible() and self.stack_view)

    def track_PC(self):
        self.ram_view.tracking = "PC"
        self.ram_view.scroll_to_item()

    def track_A(self):
        self.ram_view.tracking = "A"
        self.ram_view.scroll_to_item()

    def track_P(self):
        self.ram_view.tracking = "P"
        self.ram_view.scroll_to_item()