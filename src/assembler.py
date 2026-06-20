from src.assembler_tools.parser import Parser
from src.assembler_tools.lexer import Lexer
from src.emulator import HackEmulator

class Assembler():
    def assemble(self, emulator, input_file):

        lexer = Lexer()
        tokens = lexer.lex_file(input_file)
        symbol_table = lexer.symbol_table

        parser = Parser()
        parser.parse_tokens(emulator, tokens, symbol_table)
