from assembler.tokentype import TokenType
from assembler.lexertoken import Token

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

    
    __keywords = ["SCREEN","KBD","HEAP"]
        
    def parse_tokens(self, emulator, tokens, variable_list, label_list):
        codelines = self.__get_num_of_codelines(tokens)
        self.__remove_comments(tokens)
        self.__store_variables(emulator, tokens, variable_list, codelines)
        self.__remove_data_section(tokens)
        self.__remove_labels(tokens, label_list)
        self.__replace_pop_push_instructions(tokens)
        self.__assemble_instructions(emulator, tokens)



    def __remove_comments(self, tokens):
        for i in range(len(tokens) -1, -1, -1):
            if tokens[i][-1].get_type() == TokenType.COMMENT:
                tokens[i].pop(-1)
                if len(tokens[i]) == 0:
                    tokens.pop(i)

    def __store_variables(self, emulator, tokens, variable_list, codelines):
        static_address = codelines
        variable_table = {}
        for variable in variable_list:
            variable_table[variable] = static_address
            static_address += 1
        
        keyword_address = {"SCREEN" : 16384,
                           "KBD" : 24576}

        keyword_address["HEAP"] = codelines + len(variable_list)
        
        section = None
        for tokenline in tokens:
            if tokenline[0].get_type() == TokenType.SECTION_DECLARATION:
                section = tokenline[0].get_contents()
            elif section == "data":
                variable = tokenline[0].get_contents()
                if len(tokenline) == 1:
                    value = 0
                elif tokenline[1].get_type() == TokenType.INTEGER_LITERAL:
                    value = tokenline[1].get_contents()
                elif tokenline[1].get_type() == TokenType.KEYWORD:
                    value = keyword_address[tokenline[1].get_contents()]
                if variable not in variable_list:
                    raise SyntaxError(f"Unrecognised Variable name: {variable}")
                address = variable_table[variable]
                emulator.set_value(address, value)

            elif section == "text":
                if tokenline[0].get_contents() == "load":
                    if tokenline[1].get_contents() in variable_list:
                        variable = tokenline[1].get_contents()
                        address = variable_table[variable]
                        tokenline[1] = Token(address, TokenType.INTEGER_LITERAL)
                    elif tokenline[1].get_contents() in self.__keywords:
                        keyword = tokenline[1].get_contents()
                        address = keyword_address[keyword]
                        tokenline[1] = Token(address, TokenType.INTEGER_LITERAL)
            else:
                raise SyntaxError("Expected section declaration")

    def __remove_data_section(self, tokens):
        section = None
        i = 0
        while i < len(tokens):
            if tokens[i][0].get_type() == TokenType.SECTION_DECLARATION:
                section = tokens[i][0].get_contents()
                tokens.pop(i)
            elif section == "data":
                tokens.pop(i)
            else:
                i += 1

    def __remove_labels(self, tokens, labels_list):

        label_address = {}

        #Get address of each label
        i = 0
        while i < len(tokens):
            if tokens[i][0].get_type() == TokenType.LABEL:
                if tokens[i][0].get_contents() not in label_address:
                    label_address[tokens[i][0].get_contents()] = i
                    tokens.pop(i)
                    i -= 1
                else:
                    raise SyntaxError(f"Label: {tokens[i][0].get_contents()} has already been defined")
            i += 1

        #Replace variables with load addresses
        for tokenline in tokens:
            if tokenline[0].get_contents() == "load" and tokenline[1].get_type() == TokenType.VARIABLE_IDENTFIER:
                if tokenline[1].get_contents() in label_address:
                    address = label_address[tokenline[1].get_contents()]
                    tokenline[1] = Token(address, TokenType.INTEGER_LITERAL)
                else:
                    raise SyntaxError(f"Unrecognised label: {tokenline[1].get_contents()}")

    def __assemble_instructions(self, emulator, tokens):

        for i in range(len(tokens)):
            if tokens[i][0].get_contents() == "load":
                if tokens[i][1].get_type() != TokenType.INTEGER_LITERAL:
                    raise("load command expected Integer literal")
                emulator.set_value(i,tokens[i][1].get_contents())
            else:
                emulator.set_value(i,self.__get_instruction(tokens[i]))

    def __get_instruction(self, tokenline):
        if tokenline[1].get_contents() in ["A","M","P","S"]:
            operand = self.__operands[tokenline[1].get_contents()]
        else:
            operand = 0b00
        comp = self.__get_comp(tokenline)
        if len(tokenline) > 2:
            if tokenline[2].get_contents() in ["D","A","M","P","S"]:
                dest = self.__destinations[tokenline[2].get_contents()]
                if len(tokenline) > 3:
                    jump = self.__jumps[tokenline[3].get_contents()]
                else:
                    jump = self.__jumps["No Jump"]
            else:
                dest = self.__destinations["None"]
                jump = self.__jumps[tokenline[2].get_contents()]
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

        if tokenline[1].get_contents() in ["A","M","P","S"]:
            operand = "O"
        else:
            operand = tokenline[1].get_contents()

        return self.__instructions[tokenline[0].get_contents()][operand]

    def __replace_pop_push_instructions(self, tokens):
        for tokenline in tokens:
            if tokenline[0].get_contents() == "push":
                tokenline[0] = Token("mov",TokenType.INSTRUCTION)
                tokenline.insert(2, Token("s",TokenType.DESTINATION))
            if tokenline[0].get_contents() == "pop":
                tokenline[0] = Token("mov",TokenType.INSTRUCTION)
                tokenline.insert(1, Token("s",TokenType.OPERAND))

    def __get_num_of_codelines(self, tokens):
        codelines_count = 0
        for tokenline in tokens:
            if tokenline[0].get_type() == TokenType.INSTRUCTION:
                codelines_count += 1
        return codelines_count


