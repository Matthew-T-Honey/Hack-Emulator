from src.assembler_tools.tokentype import TokenType
from src.assembler_tools.lexertoken import Token

class Parser():
    __destinations = {"None":0b000,
                      "A":0b010,
                      "D":0b001,
                      "S":0b101,
                      "M":0b011,
                      "P":0b100}

    __jumps = {"No Jump": 0b000,
               "jgt": 0b001,
               "jeq": 0b010,
               "jge": 0b011,
               "jlt": 0b100,
               "jne": 0b101,
               "jle": 0b110,
               "jmp": 0b111}
    
    __instructions = {  "mov" :{"0" : 0b101010,
                                "1" : 0b111111,
                                "-1": 0b111010,
                                "D" : 0b001100,
                                "O" : 0b110000},
                        "not" :{"D" : 0b001101,
                                "O" : 0b110001},
                        "neg" :{"D" : 0b001111,
                                "O" : 0b110011},
                        "inc" :{"D" : 0b011111,
                                "O" : 0b110111},
                        "dec" :{"D" : 0b001110,
                                "O" : 0b110010},
                        "add" :{"O" : 0b000010},
                        "subl":{"O" : 0b010011},
                        "subr":{"O" : 0b000111},
                        "and" :{"O" : 0b000000},
                        "or"  :{"O" : 0b010101}
    }

    __operands = {"A" : 0b00,
                  "M" : 0b01,
                  "P" : 0b10,
                  "S" : 0b11}
        
    def parse_tokens(self, emulator, tokens, symbol_table):
        for i in range(emulator.memory_size):
            emulator.set_value(i,0)


        for i in range(len(tokens)):
            try:
                self.parse_line(emulator, tokens[i], i, symbol_table)
            except SyntaxError as e:
                raise SyntaxError(f"Syntax error on line {i+1}: "+str(e))

    def parse_line(self, emulator, tokenline, line_number, symbol_table):
        if len(tokenline) == 0:
            raise SyntaxError("Expected non-zero length tokenline")
        if tokenline[0].type == TokenType.INTEGER_LITERAL:
            emulator.set_value(line_number, tokenline[0].text)
        elif tokenline[0].type == TokenType.SYMBOL:
            symbol = tokenline[0].text
            if symbol in symbol_table:
                emulator.set_value(line_number, symbol_table[symbol])
            else:
                raise SyntaxError(f"Unrecognised Symbol: {symbol}")
        elif tokenline[0].type == TokenType.INSTRUCTION:
            value = self.parse_instruction(tokenline, symbol_table)
            emulator.set_value(line_number, value)
        else:
            raise SyntaxError("Expected Integer or Instruction")

    def parse_instruction(self, tokenline, symbol_table):
        if tokenline[0].text == "load":
            if tokenline[1].type == TokenType.INTEGER_LITERAL:
                return tokenline[1].text
            elif tokenline[1].type == TokenType.SYMBOL:
                symbol = tokenline[1].text
                if symbol in symbol_table:
                    return symbol_table[symbol]
                else:
                    raise SyntaxError(f"Unrecognised Symbol: {symbol}")
            else:
                raise SyntaxError("Load arguement expected type Integer_literal or Symbol")
        else:
            return self.__get_instruction(tokenline)


    def __get_instruction(self, tokenline):
        if tokenline[1].text in ["A","M","P","S"]:
            operand = self.__operands[tokenline[1].text]
        else:
            operand = 0b00
        comp = self.__get_comp(tokenline)
        if len(tokenline) > 2:
            if tokenline[2].text in ["D","A","M","P","S"]:
                dest = self.__destinations[tokenline[2].text]
                if len(tokenline) > 3:
                    jump = self.__jumps[tokenline[3].text]
                else:
                    jump = self.__jumps["No Jump"]
            else:
                dest = self.__destinations["None"]
                jump = self.__jumps[tokenline[2].text]
        else:
            dest = self.__destinations["None"]
            jump = self.__jumps["No Jump"]

        instruction = 0b1000000000000000 + (
                     (0b0000000100000000 * comp) +
                     (0b0000000001000000 * operand) + 
                     (0b0000000000001000 * dest) +
                     jump)

        return instruction
    
    def __get_comp(self, tokenline):

        if tokenline[1].text in ["A","M","P","S"]:
            operand = "O"
        else:
            operand = tokenline[1].text

        return self.__instructions[tokenline[0].text][operand]
