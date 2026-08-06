from src.H_compiler.nodetype import NodeType
from src.H_compiler.parsenode import ParseNode
from src.H_compiler.tokentype import TokenType
from src.H_compiler.token import Token

class Parser():

    __unary_operators = ["*","-","~","!"]
    __binary_operators = ["==","||","&&","|","&",
                          "<",">","<=",">=","+",
                          "-","*","/","%"]

    def __init__(self):
        self.__token_number = 0
        self.__tokens = []
        self.function_identifiers = []
        self.local_variables = {}
        self.static_variables = {}
        self.function_args = {}
        self.current_function = None


    def parse_tokens(self, tokens):
        self.__token_number = 0
        self.__tokens = tokens
        try:
            parse_tree = self.parse_code()
        except SyntaxError as e:
            raise SyntaxError(f"Parsing error on line {self.next_token().line}: {e}")
        return parse_tree, [self.function_identifiers, 
                            self.local_variables, 
                            self.static_variables, 
                            self.function_args]

    def next_token(self):
        return self.__tokens[self.__token_number]

    def look_ahead(self):
        return self.__tokens[self.__token_number+1]

    def add_next_token(self, node):
        node.add_node(self.next_token())
        self.__token_number += 1

    def parse_code(self):
        root_node = ParseNode(NodeType.CODE,self.next_token().line)

        while self.__token_number < len(self.__tokens):
            root_node.add_node(self.parse_function())

        return root_node

    def parse_function(self):
        node = ParseNode(NodeType.FUNCTION,self.next_token().line)
        if self.next_token().type not in [TokenType.VAR, TokenType.VOID]:
            raise SyntaxError("Expected 'var' or 'void'")
        self.add_next_token(node)

        if self.next_token().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function identifier")
        if self.next_token().text in self.function_identifiers:
            raise SyntaxError(f"The function {self.next_token().text} has already been defined")
        
        self.current_function = self.next_token().text
        self.function_identifiers.append(self.current_function)
        self.local_variables[self.current_function] = []
        self.static_variables[self.current_function] = []
        self.function_args[self.current_function] = []
        
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACKET:
            raise SyntaxError("Expected '('")
        self.add_next_token(node)

        node.add_node(self.parse_function_parameters())

        if self.next_token().type != TokenType.RIGHT_BRACKET:
            raise SyntaxError("Expected ')'")
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACE:
            raise SyntaxError("Expected '{'")
        self.add_next_token(node)

        while self.next_token().type != TokenType.RIGHT_BRACE:
            node.add_node(self.parse_statement())
        
        self.add_next_token(node)

        return node


    def parse_function_parameters(self):
        node = ParseNode(NodeType.PARAMETER_LIST,self.next_token().line)
        if self.next_token().type == TokenType.RIGHT_BRACKET:
            return node
        
        if self.next_token().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function parameter")
        self.function_args[self.current_function].append(self.next_token().text)
        self.add_next_token(node)

        while self.next_token().type != TokenType.RIGHT_BRACKET:
            if self.next_token().type != TokenType.COMMA:
                raise SyntaxError("Expected ','")
            self.add_next_token(node)

            if self.next_token().type != TokenType.IDENTIFIER:
                raise SyntaxError("Expected function parameter")
            self.function_args[self.current_function].append(self.next_token().text)
            self.add_next_token(node)

        return node

    
    def parse_statement(self):
        if self.next_token().type == TokenType.WHILE:
            return self.parse_while_statement()
        elif self.next_token().type == TokenType.IF:
            return self.parse_if_statement()
        elif self.next_token().type == TokenType.RETURN:
            return self.parse_return_statement()
        elif self.next_token().type in [TokenType.STATIC, TokenType.VAR]:
            return self.parse_var_declaration()
        else:
            return self.parse_expression_statement()


    def parse_while_statement(self):
        node = ParseNode(NodeType.WHILE_LOOP,self.next_token().line)
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACKET:
            raise SyntaxError("Expected '('")
        self.add_next_token(node)

        if self.next_token().type != TokenType.RIGHT_BRACKET:
            node.add_node(self.parse_expression())

        if self.next_token().type != TokenType.RIGHT_BRACKET:
            raise SyntaxError("Expected ')'")
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACE:
            raise SyntaxError("Expected '{'")
        self.add_next_token(node)

        while self.next_token().type != TokenType.RIGHT_BRACE:
            node.add_node(self.parse_statement())
        
        self.add_next_token(node)
        return node


    def parse_if_statement(self):
        node = ParseNode(NodeType.IF_CONDITION,self.next_token().line)
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACKET:
            raise SyntaxError("Expected '('")
        self.add_next_token(node)

        if self.next_token().type != TokenType.RIGHT_BRACKET:
            node.add_node(self.parse_expression())

        if self.next_token().type != TokenType.RIGHT_BRACKET:
            raise SyntaxError("Expected ')'")
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACE:
            raise SyntaxError("Expected '{'")
        self.add_next_token(node)

        while self.next_token().type != TokenType.RIGHT_BRACE:
            node.add_node(self.parse_statement())
        
        self.add_next_token(node)

        if self.next_token().type != TokenType.ELSE:
            return node
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACE:
            raise SyntaxError("Expected '{'")
        self.add_next_token(node)

        while self.next_token().type != TokenType.RIGHT_BRACE:
            node.add_node(self.parse_statement())
        
        self.add_next_token(node)

        return node


    def parse_return_statement(self):
        node = ParseNode(NodeType.RETURN_STATEMENT,self.next_token().line)
        self.add_next_token(node)

        if self.next_token().type != TokenType.SEMICOLON:
            node.add_node(self.parse_expression())

        if self.next_token().type != TokenType.SEMICOLON:
            raise SyntaxError("Expected ';'")
        self.add_next_token(node)

        return node


    def parse_var_declaration(self):
        node = ParseNode(NodeType.VAR_DECLARATION,self.next_token().line)
        static = False

        if self.next_token().type == TokenType.STATIC:
            self.add_next_token(node)
            static =  True

        if self.next_token().type != TokenType.VAR:
            raise SyntaxError("Expected keyword 'var'")
        self.add_next_token(node)

        if self.next_token().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected variable identifier")

        if (self.next_token().text in self.local_variables[self.current_function] or
            self.next_token().text in self.static_variables[self.current_function] or
            self.next_token().text in self.function_identifiers or
            self.next_token().text in self.function_args[self.current_function]):
            raise SyntaxError(f"identifier {self.next_token().text} has already been defined in this scope")
        if static:
            self.static_variables[self.current_function].append(self.next_token().text)
        else:
            self.local_variables[self.current_function].append(self.next_token().text)
        
        self.add_next_token(node)

        while self.next_token().type == TokenType.COMMA:
            self.add_next_token(node)
            if self.next_token().type != TokenType.IDENTIFIER:
                raise SyntaxError("Expected variable identifier")
            
            if (self.next_token().text in self.local_variables[self.current_function] or
                self.next_token().text in self.static_variables[self.current_function] or
                self.next_token().text in self.function_identifiers or
                self.next_token().text in self.function_args[self.current_function]):
                raise SyntaxError(f"identifier {self.next_token().text} has already been defined in this scope")
            if static:
                self.static_variables[self.current_function].append(self.next_token().text)
            else:
                self.local_variables[self.current_function].append(self.next_token().text)
            self.add_next_token(node)

        if self.next_token().type == TokenType.SEMICOLON:
            self.add_next_token()
            return node

        if self.next_token().type != TokenType.EQUALS:
            raise SyntaxError("Expected '=' or ';'")
        self.add_next_token(node)

        node.add_node(self.parse_expression())

        if self.next_token().type != TokenType.SEMICOLON:
            raise SyntaxError("Expected ';'")
        self.add_next_token(node)

        return node


    def parse_expression_statement(self):
        node = ParseNode(NodeType.EXPRESSION_STATEMENT,self.next_token().line)

        node.add_node(self.parse_expression())

        if self.next_token().type != TokenType.SEMICOLON:
            raise SyntaxError("Expected ';'")
        self.add_next_token(node)

        return node


    def parse_expression(self):
        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)

        subnode = self.parse_expression_log_or()
        if self.next_token().type != TokenType.EQUALS:
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().type == TokenType.EQUALS:
            self.add_next_token(node)
            node.add_node(self.parse_expression())
        return node

    def parse_expression_log_or(self):

        subnode = self.parse_expression_log_and()
        if self.next_token().text != "||":
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text == "||":
            self.add_next_token(node)
            node.add_node(self.parse_expression_log_or())
        return node

    
    def parse_expression_log_and(self):
        subnode = self.parse_expression_bit_or()
        if self.next_token().text != "&&":
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text == "&&":
            self.add_next_token(node)
            node.add_node(self.parse_expression_log_and())
        return node
    
    def parse_expression_bit_or(self):
        subnode = self.parse_expression_bit_and()
        if self.next_token().text != "|":
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text == "|":
            self.add_next_token(node)
            node.add_node(self.parse_expression_bit_or())
        return node
    
    def parse_expression_bit_and(self):
        subnode = self.parse_expression_eq()
        if self.next_token().text != "&":
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text == "&":
            self.add_next_token(node)
            node.add_node(self.parse_expression_bit_and())
        return node
    
    def parse_expression_eq(self):
        subnode = self.parse_expression_rel()
        if self.next_token().text != "==":
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text == "==":
            self.add_next_token(node)
            node.add_node(self.parse_expression_eq())
        return node
    
    def parse_expression_rel(self):
        subnode = self.parse_expression_add()
        if self.next_token().text not in ["<=", ">=", "<", ">"]:
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text in ["<=", ">=", "<", ">"]:
            self.add_next_token(node)
            node.add_node(self.parse_expression_rel())
        return node
    
    def parse_expression_add(self):
        subnode = self.parse_expression_mul()
        if self.next_token().text not in ["+", "-"]:
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text in ["+", "-"]:
            self.add_next_token(node)
            node.add_node(self.parse_expression_add())
        return node
    
    def parse_expression_mul(self):
        subnode = self.parse_term()
        if self.next_token().text not in ["*", "/", "%"]:
            return subnode

        node = ParseNode(NodeType.EXPRESSION,self.next_token().line)
        node.add_node(subnode)
        if self.next_token().text in ["*", "/", "%"]:
            self.add_next_token(node)
            node.add_node(self.parse_expression_mul())
        return node

    def parse_term(self):
        node = ParseNode(NodeType.TERM,self.next_token().line)
        if self.next_token().type == TokenType.INTEGER_LITERAL:
            self.add_next_token(node)
            return node
        
        if self.next_token().type == TokenType.KEYWORD:
            self.add_next_token(node)
            return node
        
        if self.next_token().type == TokenType.LEFT_BRACKET:
            self.add_next_token(node)
            node.add_node(self.parse_expression())
            if self.next_token().type != TokenType.RIGHT_BRACKET:
                raise SyntaxError("Expected ')'")
            self.add_next_token(node)
            return node

        if self.next_token().type == TokenType.OPERATOR:
            if self.next_token().text in self.__unary_operators:
                self.add_next_token(node)
                node.add_node(self.parse_term())
                return node

        if self.next_token().type == TokenType.IDENTIFIER:
            if self.look_ahead().type == TokenType.LEFT_BRACKET:
                node.add_node(self.parse_function_call())
                return node

        node.add_node(self.parse_variable())
        return node


    def parse_function_call(self):
        node = ParseNode(NodeType.FUNCTION_CALL,self.next_token().line)
        if self.next_token().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function identifier")
        if self.next_token().text not in self.function_identifiers:
            raise SyntaxError("Unrecognised function: "+self.next_token().text)
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_BRACKET:
            raise SyntaxError("Expected '('")
        self.add_next_token(node)

        if self.next_token().type == TokenType.RIGHT_BRACKET:
            self.add_next_token(node)
            return node
        
        node.add_node(self.parse_expression())
        
        while self.next_token().type != TokenType.RIGHT_BRACKET:
            if self.next_token().type != TokenType.COMMA:
                raise SyntaxError("Expected ',' or ')'")
            self.add_next_token(node)
            node.add_node(self.parse_expression())

        self.add_next_token(node)

        return node


    def parse_variable(self):
        node = ParseNode(NodeType.VARIABLE,self.next_token().line)
        if self.next_token().type == TokenType.OPERATOR:
            if self.next_token().text != "&":
                raise SyntaxError("Expected '&' or variable identifier")
            self.add_next_token(node)

        
        if self.next_token().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected variable identifier")
        if (self.next_token().text not in self.local_variables[self.current_function] and 
            self.next_token().text not in self.static_variables[self.current_function] and
            self.next_token().text not in self.function_args[self.current_function]):
            raise SyntaxError("Unrecognised variable: "+self.next_token().text)
        self.add_next_token(node)

        

        if self.next_token().type != TokenType.LEFT_SQR_BRACKET:
            return node

        node.add_node(self.parse_expression())
        if self.next_token().type != TokenType.RIGHT_SQR_BRACKET:
            raise SyntaxError("Expected ']'")
        self.add_next_token(node)

        return node


    def parse_modifiable_value(self):
        node = ParseNode(NodeType.VARIABLE,self.next_token().line)
        while self.next_token().type == TokenType.OPERATOR:
            if self.next_token().text != "*":
                raise SyntaxError("Expected identifier or '*'")
            self.add_next_token(node)

        if self.next_token().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected variable identifier")
        if (self.next_token().text not in self.local_variables[self.current_function] and
            self.next_token().text not in self.static_variables[self.current_function] and
            self.next_token().text not in self.function_args[self.current_function]):

            raise SyntaxError("Unrecognised symbol: "+self.next_token().text)
        
        self.add_next_token(node)

        if self.next_token().type != TokenType.LEFT_SQR_BRACKET:
            return node
        
        self.add_next_token(node)

        if self.next_token().type != TokenType.RIGHT_SQR_BRACKET:
            node.add_node(self.parse_expression())

        if self.next_token().type != TokenType.RIGHT_SQR_BRACKET:
            raise SyntaxError("Expected ']'")
        self.add_next_token(node)

        return node

