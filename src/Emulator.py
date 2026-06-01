from datacell import DataCell

class HackEmulator():
    __memory_locations = 32768 #The number of addressable memory locations
    __code_size = 4096 #Size of the code section
    
    def __init__(self):
        self.__D_register = DataCell()
        self.__A_register = DataCell()
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
    
    def __get_M_value(self):
        return self.get_value(self.__A_register.get_int())

    def __set_M_value(self, value):
        self.set_value(self.__A_register.get_int(), value)

    def run_program(self):
        while(self.__PC_register.get_int() < self.__code_size):
            self.__execute_command(self.__datacells[self.__PC_register.get_int()])

    def __jump(self):
        self.__PC_register.set_int(self.__A_register.get_int())

    def __execute_command(self, datacell):

        if datacell.get_bit(15) == 0:
            #A Command
            self.__A_register.set_int(datacell.get_int())
            self.__PC_register.set_int(self.__PC_register.get_int() + 1)
            return

        #Using C Command: 111a cccc ccdd djjj

        if datacell.get_bit(12) == 0:
            first_operand = self.__A_register.get_int()
        else:
            first_operand = self.__get_M_value()
        
        second_operand = self.__D_register.get_int()
        if datacell.get_bit(11) == 1:
            second_operand = 0

        if datacell.get_bit(10) == 1:
            second_operand = ~second_operand

        if datacell.get_bit(9) == 1:
            first_operand = 0

        if datacell.get_bit(8) == 1:
            first_operand = ~first_operand

        if datacell.get_bit(7) == 0:
            result = first_operand & second_operand
        else:
            result = first_operand + second_operand

        if datacell.get_bit(6) == 1:
            result = ~result

        if datacell.get_bit(3) == 1:
            self.__set_M_value(result)

        if datacell.get_bit(4) == 1:
            self.__D_register.set_int(result)

        if datacell.get_bit(5) == 1:
            self.__A_register.set_int(result)

        jump_condition = 4*datacell.get_bit(2) + 2*datacell.get_bit(1) + datacell.get_bit(0)

        if jump_condition == 1 and result > 0:
            self.__jump()
        elif jump_condition == 2 and result == 0:
            self.__jump()
        elif jump_condition == 3 and result >= 0:
            self.__jump()
        elif jump_condition == 4 and result < 0:
            self.__jump()
        elif jump_condition == 5 and result != 0:
            self.__jump()
        elif jump_condition == 6 and result <= 0:
            self.__jump()
        elif jump_condition == 7:
            self.__jump()
        else:
            self.__PC_register.set_int(self.__PC_register.get_int() + 1)

    def load_program(self, textfile):
        lines = textfile.readlines()

        for i in range(len(lines)):
            self.set_value(i, int(lines[i],2))

if __name__ == "__main__":

    testEmulator = HackEmulator()

    testcode = open("./tests/testcode.txt","r")
    testEmulator.load_program(testcode)
    testcode.close()
    print("Finished Loading")

    testEmulator.run_program()
    print("Finished Running")

    for i in range(4095, 4162):
        print(f"RAM[{i}]: {testEmulator.get_value(i)}")

