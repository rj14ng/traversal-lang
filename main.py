from lexer import Lexer
from ast import ParserState
from parser import Parser
import logging
from copy import copy

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
    with open("test.trv", 'r') as test_input:
        # State instance holds dict of variables
        state = ParserState()
        #variables = {}
        is_repeating = False
        repeat_block = []

        line_no = 0
        for line in test_input.readlines():  # Reading line-by-line
            line_no += 1
            print(f"Line no: {line_no}")
            tokens = lexer.lex(line)
            print(f"Tokens: {[token for token in copy(tokens)]}")

            if is_repeating:
                first_token = next(copy(tokens))
                if first_token.gettokentype() == 'INDENT':
                    next(tokens)  # Throw away indent token
                    repeat_block.append(tokens)
                else:
                    for i in range(0, state.repeat_count):
                        for line in repeat_block:
                            line_copy = copy(line)
                            parser.parse(line_copy, state=state).eval()
                    is_repeating = False
                    state.repeat_count = 0
                    repeat_block = []

                    parser.parse(tokens, state=state).eval()  # Parse currently held token after repeat is finished
            else:
                parser.parse(tokens, state=state).eval()
                if state.repeat_count != 0:
                    is_repeating = True

elif mode == 2:
    while True:
        line = input(">>> ")

        try:
            tokens = lexer.lex(line)
            parser.parse(tokens, state=state).eval()

        except Exception as e:
            logging.error(e)
