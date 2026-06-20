from enum import Enum

class TokenType(Enum):
    #SECTION_DECLARATION = 0 - Unused
    SYMBOL = 1    
    INTEGER_LITERAL = 2
    #LABEL = 3 - Unused
    #KEYWORD = 4 - Unused
    INSTRUCTION = 5
    OPERAND = 6
    DESTINATION = 7
    JUMP = 8
    #COMMENT = 9 - Unused
