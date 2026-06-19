from src.assembler_tools.tokentype import TokenType

class Token():
    def __init__(self, text, type):
        self.__text = text
        self.__type = type

    @property
    def text(self):
        if self.type in [TokenType.SECTION_DECLARATION, TokenType.INSTRUCTION, TokenType.JUMP]:
            return self.__text.lower()
        if self.type in [TokenType.KEYWORD, TokenType.OPERAND, TokenType.DESTINATION]:
            return self.__text.upper()
        return self.__text

    @property
    def type(self):
        return self.__type
    