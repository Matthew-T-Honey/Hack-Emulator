class Token():
    def __init__(self, text, type, line):
        self.__text = text
        self.__type = type
        self.__line_number = line

    @property
    def text(self):
        return self.__text

    @property
    def type(self):
        return self.__type

    @property
    def line(self):
        return self.line_number
    
    def __str__(self):
        return str(self.text)