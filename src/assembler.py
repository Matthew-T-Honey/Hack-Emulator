from assembler.parser import Parser
from assembler.lexer import Lexer
from emulator import HackEmulator

class Assembler():

    def assemble(self, emulator, input_file, debug = False):
        parser = Parser()
        lexer = Lexer()

        tokens, variable_list, label_list = lexer.lex_file(input_file)

        if debug:
            print("After Lexing:\n")
            for tokenlist in tokens:
                for token in tokenlist:
                    print(token.get_contents(), end = " ")
                print("")

        parser.parse_tokens(emulator, tokens, variable_list, label_list)

        if debug:
            print("\nAfter Parsing:\n")
            for tokenlist in tokens:
                for token in tokenlist:
                    print(token.get_contents(), end = " ")
                print("")



if __name__ == "__main__":
    emulator = HackEmulator()
    assembler = Assembler()

    f = open("tests/test_files/stacktest.txt","r")
    assembler.assemble(emulator, f, debug = True)
    f.close()

    print("\nBefore Running:\n")
    for i in range(128):
        print(f"RAM[{i}]: {bin(emulator.get_value(i) % 2**16)}")

    emulator.run_program(100000, debug = False, debug_ram_values = range(45,50))
    #emulator.run_program(100000)

    print("\nAfter Running:\n")
    for i in range(256):
        print(f"RAM[{i}]: {bin(emulator.get_value(i) % 2**16)}")

