from lexer import Lexer
from parser import Parser

with open("test.txt", 'r') as test_input:
    for line in test_input.readlines():  # Reading line-by-line
        # Lexer
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(line)
        
        # Parser
        pg = Parser()
        pg.parse()
        parser = pg.get_parser()
        parser.parse(tokens).eval()
