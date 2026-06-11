from parser import Parser
from lexer import Lexer

class Assembler():
    __parser = Parser()

    def __init__(self):
        self.__input_script = []

    def assemble(self, emulator):
        __lexer = Lexer()

        for line in self.__input_script:
            parsed_line, comment = self.__parser.parse_line(line)
            __lexer.lex_line(emulator, parsed_line)

    def load(self, input_file):
        lines = input_file.readlines()

        for line in lines:
            self.__input_script.append(line[:-1])




