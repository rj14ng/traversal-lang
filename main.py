from lexer import Lexer
from parser import Parser

with open("test.txt", 'r') as test_input:
    for line in test_input.readlines():
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(line)

        pg = Parser()
        pg.parse()
        parser = pg.get_parser()
        parser.parse(tokens).eval()