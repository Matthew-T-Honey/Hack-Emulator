from enum import Enum

class TokenType(Enum):
    IDENTIFIER = 0
    INTEGER_LITERAL = 1
    LEFT_BRACE = 2
    RIGHT_BRACE = 3
    LEFT_BRACKET = 4
    RIGHT_BRACKET = 5
    LEFT_SQR_BRACKET = 6
    RIGHT_SQR_BRACKET = 7
    OPERATOR = 8
    VOID = 9
    VAR = 10
    IF = 11
    ELSE = 12
    WHILE = 13
    RETURN = 14
    SEMICOLON = 15
    KEYWORD = 16
    STATIC = 17
    COMMA = 18
    EQUALS = 19

