from src.H_compiler.lexer import Lexer
from src.H_compiler.parser import Parser
from src.H_compiler.semantic_analyser import SemanticAnalyser
from src.H_compiler.generator import Generator


class Compiler():
    def compile(self, input_str):
        H_lexer = Lexer()
        tokens = H_lexer.lex_string(input_str)

        H_parser = Parser()
        parse_tree, function_data = H_parser.parse_tokens(tokens)
    
        analyser = SemanticAnalyser()
        analyser.analyse_tree(parse_tree)
    
        generator = Generator()
        code = generator.generate_code(parse_tree, function_data)
    
        return code