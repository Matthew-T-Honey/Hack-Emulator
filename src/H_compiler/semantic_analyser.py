from src.H_compiler.nodetype import NodeType
from src.H_compiler.tokentype import TokenType
from src.H_compiler.token import Token
from src.H_compiler.parsenode import ParseNode

class SemanticAnalyser():
    # Checks assignment only to modifiable values
    # Correct return types (TODO)


    def analyse_tree(self, parse_tree):
        self.analyse_node(parse_tree)

    

    def analyse_node(self, node):
        for subnode in node.nodes:
            if type(subnode) == ParseNode:
                self.check_assignment(subnode)
                self.analyse_node(subnode)



    def check_assignment(self, node):
        #Only allow term(variable) = ...
        #Or term('*', term(variable)) = ...
        #Don't allow &variable = ...
        if node.type != NodeType.EXPRESSION:
            return
        assert(len(node.nodes) in [1,3])
        if len(node.nodes) == 1:
            return
        if node.nodes[1].type != TokenType.EQUALS:
            return
        self.check_term_assignable(node.nodes[0])


    def check_term_assignable(self, node):
        if node.type != NodeType.TERM:
            raise SyntaxError(f"Analysis error on line {node.line}: Expected modifiable value")
        if type(node.nodes[0]) == Token:
            if node.nodes[0].type != TokenType.OPERATOR:
                raise SyntaxError(f"Analysis error on line {node.line}: Expected modifiable value")
            if node.nodes[0].text != "*":
                raise SyntaxError(f"Analysis error on line {node.line}: Expected modifiable value")
            self.check_term_assignable(node.nodes[1])
        elif type(node.nodes[0]) == ParseNode:
            if node.nodes[0].type != NodeType.VARIABLE:
                raise SyntaxError(f"Analysis error on line {node.line}: Expected modifiable value")
            if node.nodes[0].nodes[0].type == TokenType.OPERATOR:
                raise SyntaxError(f"Analysis error on line {node.line}: Expected modifiable value")
            return
        