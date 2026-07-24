from PyQt6 import QtCore, QtGui, QtWidgets
from src.GUI.components.error_box import ErrorBox
from src.datacell import DataCell

from src.assembler_tools.lexer import Lexer
from src.assembler_tools.parser import Parser



class RamView():


    __destinations_mapping = {0b000: "",
                                0b010: " A",
                                0b001: " D",
                                0b101: " S",
                                0b011: " M",
                                0b100: " P"}

    __jumps_mapping = {0b000: "",
                        0b001: " ;jgt",
                        0b010: " ;jeq",
                        0b011: " ;jge",
                        0b100: " ;jlt",
                        0b101: " ;jne",
                        0b110: " ;jle",
                        0b111: " ;jmp"}
    
    __instructions_mapping = {  0b101010: "mov 0",
                                0b111111: "mov 1",
                                0b111010: "mov -1",
                                0b001100: "mov D",
                                0b110000: "mov O",
                                0b001101: "not D",
                                0b110001: "not O",
                                0b001111: "neg D",
                                0b110011: "neg O",
                                0b011111: "inc D",
                                0b110111: "inc O",
                                0b001110: "dec D",
                                0b110010: "dec O",
                                0b000010: "add O",
                                0b010011: "subl O",
                                0b000111: "subr O",
                                0b000000: "and O",
                                0b010101: "or O"}

    __operands_mapping = {0b00 : "A",
                            0b01: "M",
                            0b10: "P",
                            0b11: "S"}


    def __init__(self, gui, emulator):
        self.gui = gui
        self.widget = gui.ui.RAM_view
        self.format_dropdown = gui.ui.format_dropdown
        self.reset_button = gui.ui.reset_button
        self.step_button = gui.ui.step_button
        self.run_button = gui.ui.run_button
        self.emulator = emulator
        self.speed_control = gui.speed_control
        self.RAM_search = gui.ui.RAM_search
        self.title = gui.ui.RAM_title

        self.tracking = None
        self.stack_view = True

        self.format = self.format_dropdown.currentText()

        for i in range(self.emulator.memory_size):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.widget.setItem(i, 0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.widget.setItem(i, 1, item)
            item.setText(str(i))

            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEditable|QtCore.Qt.ItemFlag.ItemIsDragEnabled|QtCore.Qt.ItemFlag.ItemIsDropEnabled|QtCore.Qt.ItemFlag.ItemIsUserCheckable|QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.widget.setItem(i, 2, item)

        self.format_dropdown.currentTextChanged.connect(self.format_changed)
        self.widget.itemClicked.connect(self.track_item)
        self.widget.itemChanged.connect(self.update_item)
        self.widget.verticalScrollBar().valueChanged.connect(self.gui.token_view.update_scrollbar)
        self.RAM_search.textChanged.connect(self.search_RAM)
        gui.ui.actionRAM_View.triggered.connect(self.toggle_visible)
        gui.ui.actionToggle_Stack_View.triggered.connect(self.toggle_stack_view)

        self.widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)

        pixmapi = QtWidgets.QStyle.StandardPixmap.SP_MediaPlay
        icon = self.gui.window.style().standardIcon(pixmapi)
        self.run_button.setIcon(icon)

        pixmapi = QtWidgets.QStyle.StandardPixmap.SP_MediaSeekForward
        icon = self.gui.window.style().standardIcon(pixmapi)
        self.step_button.setIcon(icon)

        pixmapi = QtWidgets.QStyle.StandardPixmap.SP_MediaSkipBackward
        icon = self.gui.window.style().standardIcon(pixmapi)
        self.reset_button.setIcon(icon)
        

    def search_RAM(self):
        search_text = self.RAM_search.text()
        try:
            address = int(search_text)
        except:
            return
        self.go_to_item(address)
        

    def toggle_stack_view(self):
        self.stack_view = not self.stack_view
        if self.tracking == "P":
            self.tracking = None
        self.update_RAM(self.emulator.P_value)

    def is_breakpoint(self,address):
        if address < 0 or address >= self.emulator.memory_size:
            return QtCore.Qt.CheckState.Unchecked
        return self.widget.item(address,0).checkState() == QtCore.Qt.CheckState.Checked


    def update_scrollbar(self, value):
        if value != self.widget.verticalScrollBar().value():
            self.tracking = None
            self.widget.verticalScrollBar().setValue(value)

    def update_item(self, item):
        if self.gui.execution_controller.running:
            return
        if item != self.widget.currentItem():
            return
        if item.column() != 2:
            return
        new_text = item.text()
        
        try:
            if self.format == "Binary":
                new_text = new_text.replace(" ","")
                new_val = int(new_text,2)
            elif self.format == "Decimal":
                new_val = int(new_text)
            elif self.format == "Hexadecimal":
                new_val = int(new_text,16)
            elif self.format == "Assembly":
                new_val = self.asm_to_bin(new_text)
            else:
                raise TypeError("Unknown format")
            
            if new_val >= 2**16:
                ErrorBox("Invalid RAM value on row "+str(item.row()))
            else:
                self.emulator.set_value(item.row(),new_val)
        except:
            ErrorBox("Invalid RAM value on row "+str(item.row()))
            
        self.update_RAM(item.row())
        
    def track_item(self, item):
        if item.column() == 0:
            return
        if item.row() == self.emulator.PC_value:
            self.tracking = "PC"
        elif item.row() == self.emulator.A_value:
            self.tracking = "A"
        elif item.row() == self.emulator.P_value:
            self.tracking = "P"
        else:
            self.tracking = None
        self.scroll_to_tracking()

    def go_to_item(self, address):
        self.tracking = None
        if address < 0 or address >= self.emulator.memory_size:
            return
        self.widget.scrollToItem(self.widget.item(address, 0),QtWidgets.QAbstractItemView.ScrollHint.PositionAtTop)

    def scroll_to_tracking(self):
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

        self.scroll_to_tracking()
        self.gui.screen.update_screen()
        self.gui.registers.update()

    def update_RAM(self,i):
        if i < 0 or i >= self.emulator.memory_size:
            return
        if i in [self.emulator.A_value, self.emulator.PC_value]:
            color = QtGui.QColor(255,255,50,100)
        elif i == self.emulator.P_value and self.stack_view:
            color = QtGui.QColor(255,255,50,100)
        else:
            color = QtGui.QColor(255,255,255,0)
        address_str_addition = ""
        if i == self.emulator.A_value:
            address_str_addition += " (A)"
        if i == self.emulator.P_value and self.stack_view:
            address_str_addition += " (P)"
        if i == self.emulator.PC_value:
            address_str_addition += " (PC)"

        self.widget.item(i, 0).setBackground(color)
        self.widget.item(i, 1).setBackground(color)
        self.widget.item(i, 2).setBackground(color)
        self.widget.item(i, 1).setText(str(i) + address_str_addition)
        if self.format == "Binary":
            val_string = format(self.emulator.get_value(i) % 2**16,'016b')
            val_string = val_string[:4]+" "+val_string[4:8]+" "+val_string[8:12]+" "+val_string[12:16]
        elif self.format == "Hexadecimal":
            val_string = format(self.emulator.get_value(i) % 2**16,'04X')
        elif self.format == "Decimal":
            val_string = str(self.emulator.get_value(i))
        elif self.format == "Assembly":
            val_string = self.bin_to_asm(self.emulator.get_value(i))
        else:
            raise SyntaxError("No format: "+self.format)
        self.widget.item(i, 2).setText(val_string)

        self.gui.screen.update_value(i)
        

    def format_changed(self, format):
        self.format = format
        self.update_all_RAM()
        self.gui.registers.update()
        self.gui.keyboard.update()

    
    def bin_to_asm(self, val):
        cell = DataCell()
        cell.set_int(val)
        if cell.get_bit(15) == 0:
            return "load "+str(cell.get_int())
        instruction_string = ""

        comp = 0
        for i in range(8, 14):
            comp += cell.get_bit(i) * (2**(i-8))
        if comp in self.__instructions_mapping:
            instruction_string += self.__instructions_mapping[comp]
        else:
            return format(val % 2**16,'016b')

        operand = 0
        for i in range(6, 8):
            operand += cell.get_bit(i) * (2**(i-6)) 

        if instruction_string[-1] == "O" and operand in self.__operands_mapping:
            instruction_string = instruction_string.replace("O", self.__operands_mapping[operand])

        dest = 0
        for i in range(3, 6):
            dest += cell.get_bit(i) * (2**(i-3)) 

        if dest in self.__destinations_mapping:
            instruction_string += self.__destinations_mapping[dest]

        jump = 0
        for i in range(0, 3):
            jump += cell.get_bit(i) * (2**i) 

        if jump in self.__jumps_mapping:
            instruction_string += self.__jumps_mapping[jump]

        return instruction_string
        

    def asm_to_bin(self, string):
        try:
            x = int(string,2)
            return x
        except:
            pass
        
        lexer = Lexer()
        parser = Parser()

        try:
            lexer.lex_line(".text", 0)
            tokenline = lexer.lex_line(string, 1)
        except SyntaxError as e:
            ErrorBox("Lexing Error: "+e)
            return 0
        
        try:
            val = parser.parse_instruction(tokenline, [])
        except SyntaxError as e:
            ErrorBox("Parsing Error: "+e)
            return 0
        
        return val
    
    def toggle_visible(self):
        self.widget.setVisible(not self.widget.isVisible())
        self.reset_button.setVisible(self.widget.isVisible())
        self.step_button.setVisible(self.widget.isVisible())
        self.run_button.setVisible(self.widget.isVisible())
        self.format_dropdown.setVisible(self.widget.isVisible())
        self.RAM_search.setVisible(self.widget.isVisible())
        self.title.setVisible(self.widget.isVisible())
        self.speed_control.setVisible(self.widget.isVisible())



        



    

