from src.datacell import DataCell

class HackEmulator():
    __memory_locations = 24577 #The number of addressable memory locations
    __stack_base = 16383
    
    def __init__(self):
        self.__D_register = DataCell()
        self.__A_register = DataCell()
        self.__P_register = DataCell()
        self.__P_register.set_int(self.__stack_base)
        self.__PC_register = DataCell()
        self.__datacells = []
        for i in range(self.__memory_locations):
            self.__datacells.append(DataCell())

    def set_value(self, cell, value):
        if type(cell) != int:
            raise TypeError("set_value requires type int")
        if cell < 0 or cell >= self.__memory_locations:
            raise ValueError("set_value index out of range")
        self.__datacells[cell].set_int(value)

    def get_value(self, cell):
        if type(cell) != int:
            raise TypeError("get_value requires type int")
        if cell < 0 or cell >= self.__memory_locations:
            raise ValueError("get_value index out of range")
        return self.__datacells[cell].get_int()
    
    @property
    def A_value(self):
        return self.__A_register.get_int()
    
    @property
    def D_value(self):
        return self.__D_register.get_int()
    
    @property
    def P_value(self):
        return self.__P_register.get_int()
    
    @property
    def PC_value(self):
        return self.__PC_register.get_int()
    
    @property
    def M_value(self):
        return self.get_value(self.A_value)

    @property
    def S_value(self):
        return self.get_value(self.P_value)
    
    def __set_M_value(self, value):
        self.set_value(self.A_value, value)

    def __set_S_value(self, value):
        self.set_value(self.P_value, value)

    def run_program(self, steps, debug = False, debug_ram_values = []):
        for step in range(steps):
            if debug:
                print(f"\nPC: {self.PC_value}")
                print(f"A: {self.A_value}")
                print(f"M: {self.M_value}")
                print(f"D: {self.D_value}")
                print(f"P: {self.P_value}")
                print(f"S: {self.S_value}")
                print(f"Next Command: {self.__datacells[self.PC_value].get_bin()}")
                for address in debug_ram_values:
                   print(f"RAM[{address}]: {bin(self.get_value(address) % 2**16)}")
                print(f"Stepcount: {step}")
            self.execute_next_command()

            

    def execute_next_command(self):
        datacell = self.__datacells[self.PC_value]
        if datacell.get_bit(15) == 0:
            self.__A_command(datacell)
        else:
            self.__C_command(datacell)

    def __A_command(self, datacell):
        self.__A_register.set_int(datacell.get_int())
        self.__PC_register.set_int(self.PC_value + 1)

    def __C_command(self, datacell):
        #Using C Command: 10cc cccc aadd djjj
        operand = self.__get_operand(datacell)
        result = self.__compute_result(datacell, operand)
        self.__store_result(datacell, result)
        self.__compute_jump(datacell, result)

    def __get_operand(self, datacell):
        a1 = datacell.get_bit(6)
        a2 = datacell.get_bit(7)

        if a2 == 0 and a1 == 0:
            return self.A_value
        elif a2 == 0 and a1 == 1:
            return self.M_value
        elif a2 == 1 and a1 == 0:
            return self.P_value
        elif a2 == 1 and a1 == 1:
            self.__P_register.set_int(self.P_value + 1)
            return self.S_value
        else:
            raise ValueError("Datacell bit error")

    def __compute_result(self, datacell, operand):
        first_operand = operand
        second_operand = self.D_value
        if datacell.get_bit(13) == 1:
            second_operand = 0

        if datacell.get_bit(12) == 1:
            second_operand = ~second_operand

        if datacell.get_bit(11) == 1:
            first_operand = 0

        if datacell.get_bit(10) == 1:
            first_operand = ~first_operand

        if datacell.get_bit(9) == 0:
            result = first_operand & second_operand
        else:
            result = first_operand + second_operand

        if datacell.get_bit(8) == 1:
            result = ~result
        return result

    def __store_result(self, datacell, result):

        store_condition = 4*datacell.get_bit(5) + 2*datacell.get_bit(4) + datacell.get_bit(3)

        if store_condition == 1:
            self.__D_register.set_int(result)
        elif store_condition == 2:
            self.__A_register.set_int(result)
        elif store_condition == 3:
            self.__set_M_value(result)
        elif store_condition == 4:
            self.__P_register.set_int(result)
        elif store_condition == 5:
            self.__set_S_value(result)
            self.__P_register.set_int(self.P_value - 1)
            if self.P_value > self.__stack_base:
                raise MemoryError("Stack has underflown")

    def __compute_jump(self, datacell, result):
        jump_condition = 4*datacell.get_bit(2) + 2*datacell.get_bit(1) + datacell.get_bit(0)

        if ((jump_condition == 1 and result > 0) or 
            (jump_condition == 2 and result == 0) or 
            (jump_condition == 3 and result >= 0) or 
            (jump_condition == 4 and result < 0) or 
            (jump_condition == 5 and result != 0) or 
            (jump_condition == 6 and result <= 0) or 
            (jump_condition == 7)):
            self.__jump()
        else:
            self.__PC_register.set_int(self.PC_value + 1)
    
    def __jump(self):
        self.__PC_register.set_int(self.A_value)

