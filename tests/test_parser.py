import sys
sys.path.append("..")
from src.parser import Parser

def test_basic():
    parser = Parser()
    input = "this is a string"
    output, comment = parser.parse_line(input)

    assert("this" in output)
    assert("is" in output)
    assert("a" in output)
    assert("string" in output)
    assert(len(output) == 4)
    assert(comment == "")

def test_whitespace():
    parser = Parser()
    input = "   this    is a   string   "
    output, comment = parser.parse_line(input)
    assert("this" in output)
    assert("is" in output)
    assert("a" in output)
    assert("string" in output)
    assert(len(output) == 4)
    assert(comment == "")

def test_comment():
    parser = Parser()
    input = "this is #a comment"
    output, comment = parser.parse_line(input)
    assert("this" in output)
    assert("is" in output)
    assert("a" not in output)
    assert("string" not in output)
    assert(len(output) == 2)
    assert(comment == "a comment")

    parser = Parser()
    input = "#this is a comment"
    output, comment = parser.parse_line(input)
    assert(len(output) == 0)
    assert(comment == "this is a comment")

    parser = Parser()
    input = "this is not a comment #"
    output, comment = parser.parse_line(input)
    assert(len(output) == 5)
    assert(comment == "")

def test_key_symbols():
    parser = Parser()
    input = "this is .data a com;ment #and: a .comment"
    output, comment = parser.parse_line(input)
    assert("." in output)
    assert(";" in output)
    assert(":" not in output)
    assert("com" in output)
    assert(len(output) == 8)
    assert(comment == "and: a .comment")