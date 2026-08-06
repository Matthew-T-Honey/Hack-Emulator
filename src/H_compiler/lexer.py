from src.H_compiler.tokentype import TokenType
from src.H_compiler.token import Token
import re

class Lexer():

    __special_chars = [",","=","==","(",")","{","}",
                       "[","]",";","-","~","!","||",
                       "&&","|","&","<","<=",">",
                       ">=","+","*","/","%"]

    __blocked_strings = ["if","else","while",
                         "return","true","false",
                         "heap","screen","kbd"]

    __keywords = ["true","false","null","heap","screen","kbd"]

    __operators = ["==","-","~","!","||","&&","|","&",
                  "<",">","<=",">=","+","*","/","%"]

    def lex_string(self, file_str):

        file_lines = file_str.split("\n")
        tokens = []
        for i in range(len(file_lines)):
            tokens += self.lex_line(file_lines[i], i+1)
        return tokens

    def lex_line(self, line, line_number):
        string_list = self.__remove_whitespace(line)
        token_list = []

        for string in string_list:
            token_list.append(self.lex_symbol(string, line_number))

        return token_list

    def lex_symbol(self, string, line_number):
        match string:
            case "{":
                return Token(string,TokenType.LEFT_BRACE,line_number)
            case "}":
                return Token(string,TokenType.RIGHT_BRACE,line_number)
            case "(":
                return Token(string,TokenType.LEFT_BRACKET,line_number)
            case ")":
                return Token(string,TokenType.RIGHT_BRACKET,line_number)
            case "[":
                return Token(string,TokenType.LEFT_SQR_BRACKET,line_number)
            case "]":
                return Token(string,TokenType.RIGHT_SQR_BRACKET,line_number)
            case "void":
                return Token(string,TokenType.VOID,line_number)
            case "var":
                return Token(string,TokenType.VAR,line_number)
            case "if":
                return Token(string,TokenType.IF,line_number)
            case "else":
                return Token(string,TokenType.ELSE,line_number)
            case "while":
                return Token(string,TokenType.WHILE,line_number)
            case "return":
                return Token(string,TokenType.RETURN,line_number)
            case ";":
                return Token(string,TokenType.SEMICOLON,line_number)
            case "static":
                return Token(string,TokenType.STATIC,line_number)
            case ",":
                return Token(string,TokenType.COMMA,line_number)
            case "=":
                return Token(string,TokenType.EQUALS,line_number)
        if string in self.__operators:
            return Token(string,TokenType.OPERATOR,line_number)
        if string in self.__keywords:
            return Token(string,TokenType.KEYWORD,line_number)
        if self.__is_an_integer(string):
            return Token(string,TokenType.INTEGER_LITERAL,line_number)
        if self.__is_valid_identifier(string):
            return Token(string,TokenType.IDENTIFIER,line_number)
        raise SyntaxError("Invalid symbol: "+string)



    def __remove_whitespace(self, input_line):
        input_line = input_line.replace("\n","")
        input_line = input_line.replace("\t","")
        string_list = []
        current_token = ""
        skip_char = False
        for i in range(len(input_line)):
            char = input_line[i]
            if skip_char:
                skip_char = False
            elif char == "#":
                break
            elif char == " ":
                if current_token != "":
                    string_list.append(current_token)
                current_token = ""
            elif char in self.__special_chars:
                if input_line[i:i+2] in self.__special_chars:
                    skip_char = True
                    if current_token != "":
                        string_list.append(current_token)
                    string_list.append(input_line[i:i+2])
                    current_token = ""
                else:
                    if current_token != "":
                        string_list.append(current_token)
                    string_list.append(char)
                    current_token = ""
            else:
                current_token += char
        if current_token != "":
            string_list.append(current_token)
        
        return string_list

    def __is_an_integer(self, string):
        try:
            value = int(string)
            if float(string) != value:
                return False
            return True
        except ValueError as e:
            return False

    def __is_valid_identifier(self,string):
        if not re.match("[_a-zA-Z]+[_a-zA-Z0-9]*",string):
            return False
        if string in self.__blocked_strings:
            return False
        return True
        

