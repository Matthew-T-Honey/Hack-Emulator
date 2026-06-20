from src.assembler_tools.tokentype import TokenType

class Token():
    def __init__(self, text, type):
        self.__text = text
        self.__type = type

    @property
    def text(self):
        if self.type in [TokenType.INSTRUCTION, TokenType.JUMP]:
            return self.__text.lower()
        if self.type in [TokenType.OPERAND, TokenType.DESTINATION]:
            return self.__text.upper()
        return self.__text

    @property
    def type(self):
        return self.__type
    
    def __str__(self):
        return str(self.text)
    