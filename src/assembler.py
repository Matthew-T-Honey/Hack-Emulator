from src.assembler_tools.parser import Parser
from src.assembler_tools.lexer import Lexer

class Assembler():
    def assemble(self, emulator, input_file):

        file_string = "".join(input_file.readlines())
    
        lexer = Lexer()
        tokens = lexer.lex_string(file_string)
        symbol_table = lexer.symbol_table

        parser = Parser()
        parser.parse_tokens(emulator, tokens, symbol_table)

    def assemble_line(self, emulator, line):
        pass
