import numpy as np

class DataCell():
    __size = 16 #The number of bits in the data cell
    def __init__(self):
        self.__value = np.short(0)

    def getSize(self):
        return self.__size

    def getBit(self, index):
        if type(index) != int:
            raise TypeError("getBit requires type int")
        if index < 0 or index >= self.__size:
            raise IndexError("getBit index out of range")
        if index == self.__size-1:
            mask = np.short(-2**index)
        else:
            mask = np.short(2**index)
        
        if mask & self.__value == 0:
            return 0
        return 1

    def getInt(self):
        return int(self.__value)
    
    def getBin(self):
        temp = int(self.__value) % 2**self.__size

        return bin(temp)

    def setInt(self, value):
        if type(value) != int:
            raise TypeError("setInt requires type int")
        
        value = ((value + 2**(self.__size-1)) % 2**self.__size) - 2**(self.__size-1)
        self.__value = np.short(value)

