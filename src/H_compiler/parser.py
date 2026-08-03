from src.H_compiler.nodetype import NodeType
from src.H_compiler.parsenode import ParseNode
from src.H_compiler.tokentype import TokenType

class Parser():

    def __init__(self):
        self.__token_number = 0
        self.__tokens = []


    def parse_tokens(self, tokens, symbol_table):
        self.__token_number = 0
        self.__tokens = tokens
        parse_tree = self.parse_code()

    def next_token(self):
        token = self.__tokens[self.__token_number]
        self.__token_number += 1
        return token

    def parse_code(self):
        node = ParseNode(NodeType.CODE)
        while self.__token_number < len(self.__tokens):
            node.add_node(self.parse_function())

        return node

    def parse_function(self):
        node = ParseNode(NodeType.FUNCTION)
        if self.next_token().type in [TokenType.VOID, TokenType.VAR]:
            raise SyntaxError("Expected 'var' or 'void' declaration")
        if self.next_token().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function identifier")
        if self.next_token().type != TokenType.LEFT_BRACKET:
            raise SyntaxError("Expected '('")
        if 
        
