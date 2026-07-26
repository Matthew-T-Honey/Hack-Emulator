import sys
sys.path.append("..")
from src.assembler import Assembler
from src.emulator import HackEmulator
from src.assembler_tools.lexer import Lexer
from src.assembler_tools.parser import Parser


def test_bad_code():

    emulator = HackEmulator()
    lexer = Lexer()
    parser = Parser()


    f = open("tests/test_files/invalidcode.asm","r")
    lines = f.readlines()
    f.close()

    lexer.add_keywords_to_symbol_table(1000)
    #Manually add keywords to symbol table
    #Shouldn't typically begin parsing before finishing lexing

    for i in range(len(lines)):
        try:
            tokenlist = lexer.lex_line(lines[i], i)
            if len(tokenlist) > 0:
                parser.parse_line(emulator, tokenlist, i, lexer.symbol_table)       
            #Using i for line numebr leaves gaps in the compiled code, but this doesn't matter for this purpose
            assert(lines[i].split(" ")[-1] == "#Valid\n")
        except SyntaxError as e:
            assert(lines[i].split(" ")[-1] != "#Valid\n")





