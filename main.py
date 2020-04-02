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
def next_token_type_is(tokens, type):
    '''
    Returns whether the next token type is as specified.

    Args:
        tokens (rply.lexer.LexerStream): LexerStream object containing a line of lexed tokens. This should be a *copy* of the original object, as tokens are discarded once read.
        type (string): String to match token type.
    
    Returns:
        (bool): If the token type matches 'type'.
    '''
    return next(tokens).gettokentype() == type

def find_indent_level(tokens):
    '''
    Finds the indent level of a line based on the number of INDENT tokens preceding other tokens.

    Args:
        tokens (rply.lexer.LexerStream): LexerStream object containing a line of lexed tokens. This should be a *copy* of the original object, as tokens are discarded once read.
    
    Returns:
        (int): Indent level of the current line. Returns None if line is empty.
    '''
    indent_level = 0

    while next_token_type_is(tokens, "INDENT"):
        indent_level += 1
    
    try:
        next(tokens)
        return indent_level
    except StopIteration:  # no more tokens, i.e. line is empty
        return None

def find_repeat_count(tokens):
    '''
    Returns the number of repeats as specified by a REPEAT token.

    Args:
        tokens (rply.lexer.LexerStream): LexerStream object containing a line of lexed tokens. This should be a *copy* of the original object, as tokens are discarded once read.

    Returns:
    (int): Repeat count. Returns 0 if REPEAT token not detected.

    '''
    if next_token_type_is(tokens, "REPEAT"):
        return int(next(tokens).getstr())
    else:
        return 0

def repeat(repeat_count, repeat_indent_level, input, state):
    '''
    Performs a REPEAT loop for the parse() function.

    Args:
        repeat_count (int): Number of times to repeat the code block.
        repeat_indent_level (int): The indent level of the preceding REPEAT statement.
        input (list): Sliced array passed from parse(), containing the lines of code after the REPEAT line.
        state (ast.ParserState): Parser state.
    '''
    repeat_code_block = []
    previous_indent_level = repeat_indent_level
    current_indent_level = 0
    for idx, line in enumerate(input):
        #print(f"repeat input: {input}")
        tokens = lexer.lex(line)
        current_indent_level = find_indent_level(copy(tokens))

        # If the current line is empty, let current indent level be equal to the previous indent level
        if current_indent_level is None:
            current_indent_level = previous_indent_level
        
        #print(f"repeat function: line {idx + 1}, cur ind {current_indent_level}, prev ind {previous_indent_level}")
        #print(repeat_code_block)
        
        if current_indent_level > repeat_indent_level:
            #print("CUR IND >= REPEAT IND")
            # Remove first preceding \t INDENT token and append to repeat block
            # By removing only the first token, code indented once can be run by parse() as if the indent level was 0
            # Code indented more than once is expected to be in a REPEAT loop, so the function is then recursively called again to parse nested loops
            repeat_code_block.append(line.replace('\t', '', 1))
            #print(repeat_code_block)
        else:
            #print(f"PARSING REPEAT BLOCK: {repeat_code_block}")
            for i in range(repeat_count):
                parse(repeat_code_block, state)
            return len(repeat_code_block)
            #return idx
        
        previous_indent_level = current_indent_level
    
    #print(f"REACHED END, PARSING REPEAT BLOCK: {repeat_code_block}")
    for i in range(repeat_count):
        parse(repeat_code_block, state)
    #print(f"return {len(repeat_code_block)}")
    return len(repeat_code_block)

# def repeat2(input, state):
#     repeat_code_block = []

#     tokens = lexer.lex(input[0])
#     repeat_count = find_repeat_count(copy(tokens))
#     repeat_indent_level = find_indent_level(copy(tokens))

#     previous_indent_level = repeat_indent_level
#     current_indent_level = 0
#     for idx, line in enumerate(input[1:]):
#         #print(f"repeat input: {input}")
#         tokens = lexer.lex(line)
#         current_indent_level = find_indent_level(copy(tokens))

#         # If the current line is empty, let current indent level be equal to the previous indent level
#         if current_indent_level is None:
#             current_indent_level = previous_indent_level
        
#         print(f"repeat function: line {idx + 1}, cur ind {current_indent_level}, prev ind {previous_indent_level}")
#         #print(repeat_code_block)
        
#         if current_indent_level > repeat_indent_level:
#             #print("CUR IND >= REPEAT IND")
#             # Remove first preceding \t INDENT token and append to repeat block
#             # By removing only the first token, code indented once can be run by parse() as if the indent level was 0
#             # Code indented more than once is expected to be in a REPEAT loop, so the function is then recursively called again to parse nested loops
#             repeat_code_block.append(line.replace('\t', '', 1))
#             print(repeat_code_block)
#         else:
#             #print("PARSING REPEAT BLOCK")
#             for i in range(repeat_count):
#                 parse(repeat_code_block, state)
#             break
#             #return idx
        
#         previous_indent_level = current_indent_level
    
#     print(f"return {len(repeat_code_block)-1}")
#     return len(repeat_code_block) - 1

def parse(input, state):
    '''
    Parse input from an array of strings.

    Args:
        input (list): Array containing each line of code input.
        state (ast.ParserState): Parser state.
    '''
    repeat_count = 0
    repeat_code_block = []
    previous_indent_level = 0
    current_indent_level = 0
    is_repeat_skipped = False
    lines_skipped = 0

    for idx, line in enumerate(input):
        tokens = lexer.lex(line)
        current_indent_level = find_indent_level(copy(tokens))
        # If the current line is empty, let current indent level be equal to the previous indent level
        if current_indent_level is None:
            current_indent_level = previous_indent_level
        #print(f"line {idx + 1}, cur ind {current_indent_level}, prev ind {previous_indent_level}")
        #print([token for token in tokens])
        #print(repeat_code_block)

        # if repeat_count:
        #     if not is_repeat_skipped:
        #         print("REPEAT NOT SKIPPED")
        #         is_repeat_skipped = True
        #         pass
        #     elif current_indent_level >= previous_indent_level:
        #         print("CUR IND >= PREV IND")
        #         # Remove \t tokens from string and append to repeat block
        #         repeat_code_block.append(line.replace('\t', ''))
        #     else:
        #         print("PARSING REPEAT BLOCK")
        #         for i in range(repeat_count):
        #             parse(repeat_code_block, state)
                
        #         parser.parse(tokens, state=state).eval()  # Parse currently held token after repeat is finished
        #         repeat_count = 0
        #         repeat_code_block = []
        # else:
        #     print("NORMAL PARSING")
        #     parser.parse(tokens, state=state).eval()
        #     try:
        #         repeat_count = find_repeat_count(lexer.lex(input[idx+1]))  # Peek at next line to check for REPEAT token
        #         is_repeat_skipped = False
        #     except IndexError:
        #         pass

        if lines_skipped > 0:
            #print(f"skipping lines {lines_skipped}")
            lines_skipped -= 1
            continue
        
        repeat_count = find_repeat_count(copy(tokens))
        if repeat_count:
            lines_skipped = repeat(repeat_count, current_indent_level, input[idx+1:], state)
            #print(f"lines skipped: {lines_skipped}")
        else:
            parser.parse(tokens, state=state).eval()

        # if next_token_type_is(copy(tokens), "INDENT"):
        #     lines_skipped = repeat2(input[idx-1:], state)
        # else:
        #     parser.parse(tokens, state=state).eval()
        
        previous_indent_level = current_indent_level

pg = Parser()
pg.parse()
parser = pg.get_parser()

mode = int(input("input file mode (1) or experimental repl mode (2)? "))

if mode == 0:
    with open("test.trv", 'r') as test_input:
        state = ParserState()
        parse(test_input.readlines(), state)

if mode == 1:
    with open("test.trv", 'r') as test_input:
        # State instance holds dict of variables
        state = ParserState()
        #variables = {}
        is_repeating = False
        repeat_block = []

        line_no = 0
        previous_indent_level = 0
        current_indent_level = 0
        for line in test_input.readlines():  # Reading line-by-line
            line_no += 1
            #print(f"Line no: {line_no}")
            tokens = lexer.lex(line)
            for token in tokens:
                print(f"Token type: {token.gettokentype()}")
                print(f"Token str: {token.getstr()}")
                print(f"Token pos: {token.getsourcepos()}")
            #print(f"Tokens: {[token for token in copy(tokens)]}")

            print(f"line: {line_no}, repeat stack: {state.repeat_stack}")

            previous_indent_level = current_indent_level
            current_indent_level = 0

            if is_repeating:
                tokens_copy = copy(tokens)
                while True:
                    next_token = next(tokens_copy)
                    if next_token.gettokentype() == 'INDENT':
                        current_indent_level += 1
                    else:
                        break
                print(f"current: {current_indent_level}, last: {previous_indent_level}")
                """
                # Save lines within repeat block into array, excluding the first INDENT token on each line
                first_token = next(copy(tokens))
                if first_token.gettokentype() == 'INDENT':
                    next(tokens)  # Throw away indent token
                    repeat_block.append(tokens)
                """
                if current_indent_level >= previous_indent_level:
                    for i in range(0, current_indent_level):
                        next(tokens)  # Throw away indent tokens
                    repeat_block.append(tokens)
                
                # If the first token is no longer an INDENT token, i.e. the loop has ended, parse lines in the repeat block and reset parameters
                elif current_indent_level < previous_indent_level:
                    for i in range(0, state.repeat_stack[-1]):
                        for line in repeat_block:
                            line_copy = copy(line)
                            parser.parse(line_copy, state=state).eval()
                    current_indent_level -= 1
                
                elif current_indent_level == 0:
                    is_repeating = False
                    state.repeat_stack.pop()
                    repeat_block = []
                    parser.parse(tokens, state=state).eval()  # Parse currently held token after repeat is finished
            else:
                parser.parse(tokens, state=state).eval()
                if state.repeat_stack:  # Repeat stack is not empty
                    is_repeating = True

elif mode == 2:
    while True:
        line = input(">>> ")

        try:
            tokens = lexer.lex(line)
            parser.parse(tokens, state=state).eval()

        except Exception as e:
            logging.error(e)
