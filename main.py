from src.GUI.hack_gui import HACK_GUI
from src.H_compiler.lexer import Lexer


if __name__ == "__main__":

    # gui = HACK_GUI()
    # gui.open_window()

    H_lexer = Lexer()
    f = open("tests/H_files/test_H_script.txt","r")
    input_str = "".join(f.readlines())
    tokens = H_lexer.lex_string(input_str)
    for token in tokens:
        print(token.text, token.type)
    print(H_lexer.symbol_table)