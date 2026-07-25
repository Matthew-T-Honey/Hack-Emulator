class DataCell():
    __size = 16 #The number of bits in the data cell
    __n1 = 2**(__size-1) #Precalculated values
    __n2 = 2**__size
    def __init__(self):
        self.__value = 0

    def get_size(self):
        return self.__size

    def get_bit(self, index):
        mask = 2**index
        if mask & self.__value == 0:
            return 0
        return 1

    def get_int(self):
        return self.__value
    
    def get_bin(self):
        pos_val = self.__value % self.__n2
        return bin(pos_val)

    def set_int(self, value):
        self.__value = ((value + self.__n1) % self.__n2) - self.__n1

