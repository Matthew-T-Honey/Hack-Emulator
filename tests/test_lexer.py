import sys
sys.path.append("..")
from src.assembler.lexer import Lexer

def test_basic():
    lexer = Lexer()
    input = "this is a string"
    output, comment = lexer.lex_line(input)

    assert("this" in output)
    assert("is" in output)
    assert("a" in output)
    assert("string" in output)
    assert(len(output) == 4)
    assert(comment == "")

def test_whitespace():
    lexer = Lexer()
    input = "   this    is a   string   "
    output, comment = lexer.lex_line(input)
    assert("this" in output)
    assert("is" in output)
    assert("a" in output)
    assert("string" in output)
    assert(len(output) == 4)
    assert(comment == "")

def test_comment():
    lexer = Lexer()
    input = "this is #a comment"
    output, comment = lexer.lex_line(input)
    assert("this" in output)
    assert("is" in output)
    assert("a" not in output)
    assert("string" not in output)
    assert(len(output) == 2)
    assert(comment == "a comment")

    lexer = Lexer()
    input = "#this is a comment"
    output, comment = lexer.lex_line(input)
    assert(len(output) == 0)
    assert(comment == "this is a comment")

    lexer = Lexer()
    input = "this is not a comment #"
    output, comment = lexer.lex_line(input)
    assert(len(output) == 5)
    assert(comment == "")

def test_key_symbols():
    lexer = Lexer()
    input = "this is .data a com;ment #and: a .comment"
    output, comment = lexer.lex_line(input)
    assert("." in output)
    assert(";" in output)
    assert(":" not in output)
    assert("com" in output)
    assert(len(output) == 8)
    assert(comment == "and: a .comment")