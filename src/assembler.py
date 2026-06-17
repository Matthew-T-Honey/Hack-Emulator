from src.assembler_tools.parser import Parser
from src.assembler_tools.lexer import Lexer
from src.emulator import HackEmulator

class Assembler():

    def assemble(self, emulator, input_file, debug = False):
        parser = Parser()
        lexer = Lexer()

        tokens = lexer.lex_file(input_file)

        if debug:
            print("After Lexing:\n")
            for tokenlist in tokens:
                for token in tokenlist:
                    print(token.get_contents(), end = " ")
                print("")

        parser.parse_tokens(emulator, tokens)

        if debug:
            print("\nAfter Parsing:\n")
            for tokenlist in tokens:
                for token in tokenlist:
                    print(token.get_contents(), end = " ")
                print("")
