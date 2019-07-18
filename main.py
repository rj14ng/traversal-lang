from lexer import Lexer
from ast import ParserState
from parser import Parser

# Parser state
state = ParserState()

# Lexer
lexer = Lexer().get_lexer()

# Parser
pg = Parser()
pg.parse()
parser = pg.get_parser()

mode = int(input("input file mode (1) or experimental repl mode (2)? "))

if mode == 1:
    with open("test.txt", 'r') as test_input:
        # State instance holds dict of variables
        state = ParserState()
        variables = {}

        for line in test_input.readlines():  # Reading line-by-line
            tokens = lexer.lex(line)
            parser.parse(tokens, state=state).eval()

elif mode == 2:
    while True:
        line = input(">>> ")

        try:
            tokens = lexer.lex(line)
            parser.parse(tokens, state=state).eval()

        except Exception as e:
            print(e)  # Probably need better error reporting in the future
