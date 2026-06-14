from enum import Enum

class TokenType(Enum):
    SECTION_DECLARATION = 0
    VARIABLE_IDENTFIER = 1    
    INTEGER_LITERAL = 2
    LABEL = 3
    KEYWORD = 4
    INSTRUCTION = 5
    OPERAND = 6
    DESTINATION = 7
    JUMP = 8
    COMMENT = 9
