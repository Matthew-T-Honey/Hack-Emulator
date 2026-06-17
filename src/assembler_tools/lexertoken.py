from src.assembler_tools.tokentype import TokenType

class Token():
    def __init__(self, contents, type):
        self.__contents = contents
        self.__type = type

    def get_contents(self):
        if self.__type in [TokenType.SECTION_DECLARATION, TokenType.INSTRUCTION, TokenType.JUMP]:
            return self.__contents.lower()
        if self.__type in [TokenType.KEYWORD, TokenType.OPERAND, TokenType.DESTINATION]:
            return self.__contents.upper()
        return self.__contents

    def get_type(self):
        return self.__type
    