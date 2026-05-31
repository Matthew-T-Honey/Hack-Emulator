import DataCell as DataCell

class HackEmulator():
    __memoryLocations = 32768 #The number of addressable memory locations
    __codeSize = 4096
    
    def __init__(self):
        self.__Dregister = 0
        self.__Aregister = 0
        self.__PCregister = 0
        self.__datacells = []
        for i in range(self.__memoryLocations):
            self.__datacells.append(DataCell.DataCell())

    def setValue(self, cell, value):
        if type(cell) != int:
            raise TypeError("setValue requires type int")
        if cell < 0 or cell >= self.__memoryLocations:
            raise ValueError("setValue index out of range")
        self.__datacells[cell].setInt(value)

    def getValue(self, cell):
        if type(cell) != int:
            raise TypeError("getValue requires type int")
        if cell < 0 or cell >= self.__memoryLocations:
            raise ValueError("getValue index out of range")
        return self.__datacells[cell].getInt()
    
    def __getMValue(self):
        return self.getValue(self.__Aregister)

    def __setMValue(self, value):
        self.setValue(self.__Aregister, value)

    def runProgram(self):
        while(self.__PCregister < self.__codeSize):
            
            #print(f"\nCommand: {self.__datacells[self.__PCregister].getBin()}")
            self.__executeCommand(self.__datacells[self.__PCregister])
            #print(f"PC: {self.__PCregister}")
            #print(f"A: {self.__Aregister}")
            #print(f"D: {self.__Dregister}")

    def __jump(self):
        self.__PCregister = self.__Aregister

    def __executeCommand(self, dataCell):

        if dataCell.getBit(15) == 0:
            #A Command
            self.__Aregister = dataCell.getInt()
            self.__PCregister += 1
            return

        #Using C Command: 111a cccc dddc cjjj

        if dataCell.getBit(12) == 0:
            firstOperand = self.__Aregister
        else:
            firstOperand = self.__getMValue()
        
        secondOperand = self.__Dregister
        if dataCell.getBit(11) == 1:
            secondOperand = 0

        if dataCell.getBit(10) == 1:
            secondOperand = ~secondOperand

        if dataCell.getBit(9) == 1:
            firstOperand = 0

        if dataCell.getBit(8) == 1:
            firstOperand = ~firstOperand

        if dataCell.getBit(7) == 0:
            result = firstOperand & secondOperand
        else:
            result = firstOperand + secondOperand

        if dataCell.getBit(6) == 1:
            result = ~result

        if dataCell.getBit(3) == 1:
            self.__setMValue(result)

        if dataCell.getBit(4) == 1:
            self.__Dregister = result

        if dataCell.getBit(5) == 1:
            self.__Aregister = result

        jumpCondition = 4*dataCell.getBit(2) + 2*dataCell.getBit(1) + dataCell.getBit(0)

        if jumpCondition == 1 and result > 0:
            self.__jump()
        elif jumpCondition == 2 and result == 0:
            self.__jump()
        elif jumpCondition == 3 and result >= 0:
            self.__jump()
        elif jumpCondition == 4 and result < 0:
            self.__jump()
        elif jumpCondition == 5 and result != 0:
            self.__jump()
        elif jumpCondition == 6 and result <= 0:
            self.__jump()
        elif jumpCondition == 7:
            self.__jump()
        else:
            self.__PCregister += 1

    def loadProgram(self, textfile):
        lines = textfile.readlines()

        for i in range(len(lines)):
            self.setValue(i, int(lines[i],2))
            #print(f"Loaded {bin(int(lines[i],2))}")
            #print(f"Stored as {self.getValue(i)}")


if __name__ == "__main__":

    testEmulator = HackEmulator()

    testcode = open("./test/testcode.txt","r")
    testEmulator.loadProgram(testcode)
    testcode.close()
    print("Finished Loading")

    testEmulator.runProgram()
    print("Finished Running")

    for i in range(4095, 4162):
        print(f"RAM[{i}]: {testEmulator.getValue(i)}")

