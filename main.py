from lexer import Lexer
from ast import ParserState
from parser import Parser
import logging
import sys
from copy import copy

# Parse functions
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


def repeat(repeat_count, repeat_indent_level, input, start_lineno, state):
    '''
    Performs a REPEAT loop for the parse() function.

    Args:
        repeat_count (int): Number of times to repeat the code block.
        repeat_indent_level (int): The indent level of the preceding REPEAT statement.
        input (list): Sliced array passed from parse(), containing the lines of code after the REPEAT line.
        state (ast.ParserState): Parser state.
    
    Returns:
        (int): Number of lines within the repeat block, which parse() will have to skip.
    '''
    repeat_code_block = []
    previous_indent_level = repeat_indent_level
    current_indent_level = 0
    for line in input:
        tokens = lexer.lex(line)
        current_indent_level = find_indent_level(copy(tokens))

        # If the current line is empty, let current indent level be equal to the previous indent level
        if current_indent_level is None:
            current_indent_level = previous_indent_level
        
        if current_indent_level > repeat_indent_level:
            # Remove first preceding \t INDENT token and append to repeat block
            # By removing only the first token, code indented once can be run by parse() as if the indent level was 0
            # Code indented more than once is expected to be in a REPEAT loop, so the function is then recursively called again to parse nested loops
            repeat_code_block.append(line.replace('\t', '', 1))
        else:
            # Perform loop once current indent level returns to the REPEAT statement's indent level
            for i in range(repeat_count):
                parse(repeat_code_block, start_lineno, state)
            
            return len(repeat_code_block)
        
        previous_indent_level = current_indent_level
    
    # Perform loop if the repeat code block ends up being the same as the input
    # This occurs for deeply nested loops
    for i in range(repeat_count):
        parse(repeat_code_block, start_lineno, state)

    return len(repeat_code_block)


def repeatuntil(repeat_indent_level, input, start_lineno, state):
    '''
    Performs a REPEATUNTIL loop for the parse() function.

    Args:
        repeat_indent_level (int): The indent level of the preceding REPEAT statement.
        input (list): Sliced array passed from parse(), containing the lines of code including and after the REPEAT line.
        state (ast.ParserState): Parser state.
    
    Returns:
        (int): Number of lines within the repeat block, which parse() will have to skip.
    '''
    repeat_code_block = []
    previous_indent_level = repeat_indent_level
    current_indent_level = 0

    # Keep the tokens in the repeat statement for further parsing
    repeatuntil_tokens = lexer.lex(input[0])

    for line in input[1:]:  # Skip over repeat line
        tokens = lexer.lex(line)
        current_indent_level = find_indent_level(copy(tokens))

        # If the current line is empty, let current indent level be equal to the previous indent level
        if current_indent_level is None:
            current_indent_level = previous_indent_level
        
        if current_indent_level > repeat_indent_level:
            # Remove first preceding \t INDENT token and append to repeat block
            # By removing only the first token, code indented once can be run by parse() as if the indent level was 0
            # Code indented more than once is expected to be in a REPEAT loop, so the function is then recursively called again to parse nested loops
            repeat_code_block.append(line.replace('\t', '', 1))
        else:
            # Parse REPEATUNTIL condition to gauge if the condition is satisfied or not
            repeatuntil_condition = parser.parse(copy(repeatuntil_tokens), state=state).eval()

            # Perform loop once current indent level returns to the REPEAT statement's indent level
            while not repeatuntil_condition.value:
                parse(repeat_code_block, start_lineno, state)
                repeatuntil_condition = parser.parse(copy(repeatuntil_tokens), state=state).eval()
            
            return len(repeat_code_block)
        
        previous_indent_level = current_indent_level
    
    # Perform loop if the repeat code block ends up being the same as the input
    # This occurs for deeply nested loops
    repeatuntil_condition = parser.parse(copy(repeatuntil_tokens), state=state).eval()

    while not repeatuntil_condition:
        parse(repeat_code_block, start_lineno, state)
        repeatuntil_condition = parser.parse(copy(repeatuntil_tokens), state=state).eval()
    
    return len(repeat_code_block)


def parse(input, start_lineno, state):
    '''
    Parse input from an array of strings.

    Args:
        input (list): Array containing each line of code input.
        state (ast.ParserState): Parser state.
    '''
    repeat_count = 0
    previous_indent_level = 0
    current_indent_level = 0
    lines_skipped = 0

    for idx, line in enumerate(input):
        tokens = lexer.lex(line)
        lineno = idx + start_lineno
        current_indent_level = find_indent_level(copy(tokens))

        # If the current line is empty, let current indent level be equal to the previous indent level
        if current_indent_level is None:
            current_indent_level = previous_indent_level

        if lines_skipped > 0:
            lines_skipped -= 1
            continue
        
        # REPEAT statement found
        if next_token_type_is(copy(tokens), "REPEAT"):
            try:
                repeat_count = parser.parse(tokens, state=state)  # Don't .eval() as this returns an int?
            except:
                print(f"On line {lineno}:", end=' ')
                raise
            lines_skipped = repeat(repeat_count, current_indent_level, input[idx+1:], lineno + 1, state)
        # REPEATUNTIL statement found
        elif next_token_type_is(copy(tokens), "REPEATUNTIL"):
            try:
                repeat_count = parser.parse(tokens, state=state)
            except:
                print(f"On line {lineno}:", end=' ')
                raise
            lines_skipped = repeatuntil(current_indent_level, input[idx:], lineno + 1, state)
        # Normal statement parsed using RPLY's native parser
        else:
            try:
                parser.parse(tokens, state=state).eval()
            except:
                print(f"On line {lineno}:", end=' ')
                raise
        
        previous_indent_level = current_indent_level


if __name__ == "__main__":
    # Remove Python traceback to hide 'scary' error messages
    sys.tracebacklimit = 0

    # Parser state
    state = ParserState()

    # Lexer
    lexer = Lexer().get_lexer()

    # Parser
    pg = Parser()
    pg.parse()
    parser = pg.get_parser()

    # Open and parse test.trv file
    with open("test.trv", 'r') as test_input:
        state = ParserState()
        parse(test_input.readlines(), 1, state)
