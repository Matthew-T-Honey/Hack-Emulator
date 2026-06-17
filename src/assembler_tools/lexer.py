from src.assembler_tools.tokentype import TokenType
from src.assembler_tools.lexertoken import Token


class Lexer():

    __instructions = ["load",
                    "mov",
                    "inc",
                    "dec",
                    "neg",
                    "not",
                    "add",
                    "subl",
                    "subr",
                    "and",
                    "or",
                    "push",
                    "pop"]
    
    __operands = ["a","d","m","s","p","1","0","-1"]
    __destinations = ["a","d","m","p","s"]
    __jumps = ["jlt", "jeq", "jgt", "jle", "jne", "jge", "jmp"]
    __keywords = ["screen", "kbd", "heap"]

    def __init__(self):
        self.__section_type = None

    def lex_file(self, file):
        self.__section_type = None

        file_tokens = []
        file_lines = file.readlines()

        for i in range(len(file_lines)):
            line = file_lines[i]
            try:
                line_tokens = self.__lex_line(line)
            except SyntaxError as e:
                raise SyntaxError(f"Syntax error on line {i+1}: "+str(e))
            if line_tokens != []:
                file_tokens.append(line_tokens)

        return file_tokens
    
    def __lex_line(self, line):
        
        string_list, comment = self.__split_line(line)
        tokenlist = self.__form_tokenlist(string_list)

        if comment != "":
            comment_token = Token(comment, TokenType.COMMENT)
            tokenlist.append(comment_token)

        return tokenlist

    def __split_line(self, input_line):
        input_line = input_line.replace("\n","")
        input_line = input_line.replace("\t","")
        string_list = []
        comment = ""
        is_comment = False
        current_token = ""
        for char in input_line:
            if is_comment:
                comment += char
            elif char == "#":
                is_comment = True
            elif char == " ":
                if current_token != "":
                    string_list.append(current_token)
                current_token = ""
            elif char in [";",":","."]:
                if current_token != "":
                    string_list.append(current_token)
                string_list.append(char)
                current_token = ""
            else:
                current_token += char
        if current_token != "":
            string_list.append(current_token)
        
        return string_list, comment
        

    def __form_tokenlist(self, string_list):
        if len(string_list) == 0:
            #Empty line
            return []

        if string_list[0] == ".":
            #SECTION DECLARATION
            return self.__lex_section_declaration(string_list)
        
        if self.__section_type == None:
            #No section has been declared
            raise SyntaxError("No section type has been declared")

        if self.__section_type == "data":
            #VARIABLE DECLARATION
            return self.__lex_variable_declaration(string_list)
        
        if string_list[0].lower() not in self.__instructions:
            #LABEL DECLARATION
            return self.__lex_label_declaration(string_list)

        if string_list[0].lower() == "load":
            #LOAD INSTRUCTION
            return self.__lex_load_instruction(string_list)
        
        if string_list[0].lower() == "push":
            #Push INSTRUCTION
            return self.__lex_push_instruction(string_list)

        if string_list[0].lower() == "pop":
            #Pop INSTRUCTION
            return self.__lex_pop_instruction(string_list)
        
        if string_list[0].lower() == "mov":
            #Mov INSTRUCTION
            return self.__lex_mov_instruction(string_list)
        
        if string_list[0].lower() in ["inc", "dec", "neg", "not"]:
            #Unary INSTRUCTION
            return self.__lex_unary_instruction(string_list)
        
        if string_list[0].lower() in ["add", "subl", "subr", "and", "or"]:
            #Binary INSTRUCTION
            return self.__lex_binary_instruction(string_list)

        raise SyntaxError("Unrecognised Command")

    def __lex_section_declaration(self, string_list):

        if len(string_list) != 2:
            raise SyntaxError("Expected a section declaration")
        if string_list[1].lower() not in ["data", "text"]:
            raise SyntaxError(f"Invalid section type: {string_list[1]}")
        self.__section_type = string_list[1].lower()

        return [Token(string_list[1].lower(), TokenType.SECTION_DECLARATION)]

    
    def __lex_variable_declaration(self, string_list):
        tokenlist = []
        if self.__is_a_blocked_string(string_list[0]):
            raise SyntaxError(f"Invalid variable name: {string_list[0]}")

        if len(string_list) == 1:
            return [Token(string_list[0], TokenType.VARIABLE_IDENTFIER)]
        if len(string_list) != 3:
            raise SyntaxError("Invalid variable declaration")
        if string_list[1] != ":":
            raise SyntaxError("Invalid variable declaration")
        
        tokenlist.append(Token(string_list[0], TokenType.VARIABLE_IDENTFIER))
        if self.__is_an_integer(string_list[2]):
            tokenlist.append(Token(int(string_list[2]), TokenType.INTEGER_LITERAL))
        elif string_list[2].lower() in self.__keywords:
            tokenlist.append(Token(string_list[2].lower(), TokenType.KEYWORD))
        else:
            raise SyntaxError("Expected an integer value")

        return tokenlist

    def __lex_label_declaration(self, string_list):
        if len(string_list) != 2:
            raise SyntaxError("Invalid label declaration")
        if string_list[1] != ":":
            raise SyntaxError("Invalid label declaration")
        
        if self.__is_a_blocked_string(string_list[0]):
            raise SyntaxError(f"Invalid label name: {string_list[0]}")

        return [Token(string_list[0], TokenType.LABEL)]

    def __lex_load_instruction(self, string_list):
        tokenlist = []
        if len(string_list) != 2:
            raise SyntaxError("Invalid load declaration")
        tokenlist.append(Token("load", TokenType.INSTRUCTION))
        if self.__is_an_integer(string_list[1]):
            if int(string_list[1]) < 0:
                raise SyntaxError("Load requires a positive value")
            tokenlist.append(Token(int(string_list[1]), TokenType.INTEGER_LITERAL))
        elif string_list[1].lower() in self.__keywords:
            tokenlist.append(Token(string_list[1].lower(), TokenType.KEYWORD))
        else:
            tokenlist.append(Token(string_list[1], TokenType.VARIABLE_IDENTFIER)) #This could be a variable identifier or a label
                                                                                  #The correctness of this name is verified in the parser
        return tokenlist

    def __lex_push_instruction(self, string_list):
        tokenlist = []
        if len(string_list) < 2:
            raise SyntaxError("Invalid push instruction")
        if string_list[1].lower() not in self.__operands:
            raise SyntaxError("Invalid push instruction")
        tokenlist.append(Token("push", TokenType.INSTRUCTION))
        tokenlist.append(Token(string_list[1].lower(), TokenType.OPERAND))

        tokenlist += self.__lex_jump(string_list[2:])
        
        return tokenlist

    def __lex_pop_instruction(self, string_list):
        tokenlist = []
        tokenlist.append(Token("pop", TokenType.INSTRUCTION))
        tokenlist += self.__lex_dest_and_jump(string_list[1:])

        return tokenlist

    def __lex_mov_instruction(self, string_list):
        tokenlist = []
        if len(string_list) < 2:
            raise SyntaxError("Invalid mov instruction")
        if string_list[1].lower() not in self.__operands:
            raise SyntaxError("Invalid mov instruction")
        tokenlist.append(Token("mov", TokenType.INSTRUCTION))
        tokenlist.append(Token(string_list[1].lower(), TokenType.OPERAND))

        tokenlist += self.__lex_dest_and_jump(string_list[2:])
        
        return tokenlist

    def __lex_unary_instruction(self, string_list):
        tokenlist = []
        if len(string_list) < 2:
            raise SyntaxError("Invalid unary instruction")
        if string_list[1].lower() not in ["a","d","m","p","s"]:
            raise SyntaxError("Invalid unary instruction")
        tokenlist.append(Token(string_list[0].lower(), TokenType.INSTRUCTION))
        tokenlist.append(Token(string_list[1].lower(), TokenType.OPERAND))

        tokenlist += self.__lex_dest_and_jump(string_list[2:])
        
        return tokenlist

    def __lex_binary_instruction(self, string_list):
        tokenlist = []
        if len(string_list) < 2:
            raise SyntaxError("Invalid binary instruction")
        if string_list[1].lower() not in ["a","m","p","s"]:
            raise SyntaxError("Invalid binary instruction")
        tokenlist.append(Token(string_list[0].lower(), TokenType.INSTRUCTION))
        tokenlist.append(Token(string_list[1].lower(), TokenType.OPERAND))

        tokenlist += self.__lex_dest_and_jump(string_list[2:])
        
        return tokenlist        

    def __lex_dest_and_jump(self, string_list):
        tokenlist = []
        if len(string_list) > 0 and string_list[0] != ";":
            if string_list[0].lower() not in self.__destinations:
                raise SyntaxError("Invalid destination")
            tokenlist.append(Token(string_list[0].lower(), TokenType.DESTINATION))
            tokenlist += self.__lex_jump(string_list[1:])
        else:
            tokenlist += self.__lex_jump(string_list)
        
        return tokenlist

    def __lex_jump(self, string_list):
        if len(string_list) == 0:
            return []
        if len(string_list) != 2:
            raise SyntaxError("Invalid jump instruction")
        if string_list[0] != ";":
            raise SyntaxError("Invalid jump instruction")
        if string_list[1].lower() not in self.__jumps:
            raise SyntaxError("Invalid jump instruction")
        return [Token(string_list[1].lower(), TokenType.JUMP)]


    def __is_an_integer(self, string):
        try:
            value = int(string)
            if float(string) != value:
                return False
            return True
        except ValueError as e:
            return False

    def __is_a_blocked_string(self, string):
        if self.__is_an_integer(string):
            return True
        if string.lower() in self.__instructions:
            return True
        if string.lower() in self.__operands:
            return True
        if string.lower() in self.__jumps:
            return True
        if string.lower() in self.__keywords:
            return True
        return False
