class Parser():
    __keysymbols = [";",":","."]
    __comment_char = "#"
    def parse_line(self, input_str):
        token_list = []
        comment = ""
        is_comment = False
        current_token = ""
        for char in input_str:
            if is_comment:
                comment += char
            elif char == self.__comment_char:
                is_comment = True
            elif char == " ":
                if current_token != "":
                    token_list.append(current_token)
                current_token = ""
            elif char in self.__keysymbols:
                if current_token != "":
                    token_list.append(current_token)
                token_list.append(char)
                current_token = ""
            else:
                current_token += char
        if current_token != "":
            token_list.append(current_token)
        
        return token_list, comment


