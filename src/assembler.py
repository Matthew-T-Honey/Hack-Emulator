from src.assembler_tools.parser import Parser
from src.assembler_tools.lexer import Lexer
from src.emulator import HackEmulator

class Assembler():
    def assemble(self, emulator, input_file):
        tokens = self.get_tokens(input_file)
        self.parse_tokens(emulator, tokens)

    def get_tokens(self, input_file):
        lexer = Lexer()
        return lexer.lex_file(input_file)
    
    def parse_tokens(self, emulator, tokens):
        parser = Parser()
        parser.parse_tokens(emulator, tokens)
