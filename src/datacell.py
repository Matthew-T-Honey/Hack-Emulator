import numpy as np

class DataCell():
    __size = 16 #The number of bits in the data cell
    def __init__(self):
        self.__value = np.short(0)

    def get_size(self):
        return self.__size

    def get_bit(self, index):
        if type(index) != int:
            raise TypeError("get_bit requires type int")
        if index < 0 or index >= self.__size:
            raise IndexError("get_bit index out of range")
        if index == self.__size-1:
            mask = np.short(-2**index)
        else:
            mask = np.short(2**index)
        
        if mask & self.__value == 0:
            return 0
        return 1

    def get_int(self):
        return int(self.__value)
    
    def get_bin(self):
        pos_val = int(self.__value) % 2**self.__size

        return bin(pos_val)

    def set_int(self, value):
        if type(value) != int:
            raise TypeError("set_int requires type int")
        
        value = ((value + 2**(self.__size-1)) % 2**self.__size) - 2**(self.__size-1)
        self.__value = np.short(value)

