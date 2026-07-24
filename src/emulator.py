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
        self.RAM_edit = None

    def reset(self):
        self.__D_register.set_int(0)
        self.__A_register.set_int(0)
        self.__P_register.set_int(self.__stack_base)
        self.__PC_register.set_int(0)
        for i in range(self.__memory_locations):
            self.__datacells[i].set_int(0)


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
    def memory_size(self):
        return self.__memory_locations
    
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
        if self.__A_register.get_int() >= self.__memory_locations or self.__A_register.get_int() < 0:
            return 0
        return self.get_value(self.__A_register.get_int())

    @property
    def S_value(self):
        if self.__P_register.get_int() >= self.__memory_locations or self.__P_register.get_int() < 0:
            return 0
        return self.get_value(self.__P_register.get_int())
    
    def __set_M_value(self, value):
        if self.__A_register.get_int() >= self.__memory_locations or self.__A_register.get_int() < 0:
            raise ValueError(f"Cannot set M value for address: {self.__A_register.get_int()}")
        self.set_value(self.__A_register.get_int(), value)

    def __set_S_value(self, value):
        if self.__P_register.get_int() >= self.__memory_locations or self.__P_register.get_int() < 0:
            raise ValueError(f"Cannot set S value for address: {self.__P_register.get_int()}")
        self.set_value(self.__P_register.get_int(), value)

    def run_program(self, steps):
        for step in range(steps):
            self.execute_next_command()

            

    def execute_next_command(self):
        self.RAM_edit = None
        datacell = self.__datacells[self.__PC_register.get_int()]
        if datacell.get_bit(15) == 0:
            self.__A_command(datacell)
        else:
            self.__C_command(datacell)
        if self.__PC_register.get_int() < 0:
            self.__PC_register.set_int(0)
            raise ValueError("PC register value outside acceptable range")
        if self.__PC_register.get_int() >= self.__memory_locations:
            self.__PC_register.set_int(self.__memory_locations-1)
            raise ValueError("PC register value outside acceptable range")
        return self.RAM_edit

    def __A_command(self, datacell):
        self.__A_register.set_int(datacell.get_int())
        self.__PC_register.set_int(self.__PC_register.get_int() + 1)

    def __C_command(self, datacell):
        #Using C Command: 10cc cccc aadd djjj
        operand = self.__get_operand(datacell)
        result = self.__compute_result(datacell, operand)
        self.__store_result(datacell, result)
        self.__compute_jump(datacell, result)

    def __get_operand(self, datacell):
        operand_condition = 2*datacell.get_bit(7) + datacell.get_bit(6)

        if operand_condition == 0:
            return self.__A_register.get_int()
        if operand_condition == 1:
            return self.M_value
        if operand_condition == 2:
            return self.__P_register.get_int()
        if operand_condition == 3:
            self.__P_register.set_int(self.__P_register.get_int() + 1)
            return self.S_value
        raise ValueError("Datacell bit error")

    def __compute_result(self, datacell, operand):
        first_operand = operand
        second_operand = self.__D_register.get_int()
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
            self.RAM_edit = self.__A_register.get_int()
        elif store_condition == 4:
            self.__P_register.set_int(result)
        elif store_condition == 5:
            self.__set_S_value(result)
            self.RAM_edit = self.__P_register.get_int()
            self.__P_register.set_int(self.__P_register.get_int() - 1)
            if self.__P_register.get_int() > self.__stack_base:
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
            self.__PC_register.set_int(self.__PC_register.get_int() + 1)
    
    def __jump(self):
        self.__PC_register.set_int(self.__A_register.get_int())

