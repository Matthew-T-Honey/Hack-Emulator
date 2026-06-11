class Lexer():
    __section_types = ["data", "text"]

    __operands = ["D","A","M","P","S","1","0","-1"]
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
    
    __keywords = ["FP","SCREEN","KBD"]
    for i in range(16):
        __keywords.append("R"+str(i))

    def __init__():
        __section = None
        __symbol_table = []
        
    
    def lex_line(self, line, emulator):
        if line[0] == ".":
            if len(line) != 2:
                raise SyntaxError(f"Expected .{self.__section_types[0]} or .{self.__section_types[1]}")
            if line[1] in self.__section_types:
                self.__section = line[1]
                return
            else:
                raise SyntaxError(f"Expected .{self.__section_types[0]} or .{self.__section_types[1]}")
        if self.__section == None:
            raise SyntaxError("Expected section declaration")



    def mov_instruction(self, line, emulator):
        pass
        
    def inc_instruction(self, line, emulator):
        pass

    def dec_instruction(self, line, emulator):
        pass

    def neg_instruction(self, line, emulator):
        pass

    def not_instruction(self, line, emulator):
        pass

    def add_instruction(self, line, emulator):
        pass

    def subl_instruction(self, line, emulator):
        pass

    def subr_instruction(self, line, emulator):
        pass

    def and_instruction(self, line, emulator):
        pass

    def or_instruction(self, line, emulator):
        pass

    def push_instruction(self, line, emulator):
        pass

    def pop_instruction(self, line, emulator):
        pass

    __c_instructions = {"mov":  mov_instruction, 
                        "inc":  inc_instruction, 
                        "dec":  dec_instruction, 
                        "neg":  neg_instruction, 
                        "not":  not_instruction, 
                        "add":  add_instruction, 
                        "subl": subl_instruction, 
                        "subr": subr_instruction, 
                        "and":  and_instruction, 
                        "or":   or_instruction, 
                        "push": push_instruction, 
                        "pop":  pop_instruction}