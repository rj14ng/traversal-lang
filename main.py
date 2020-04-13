from lexer import Lexer
from ast import ParserState
from parser import Parser
import logging
import sys
from copy import copy
import time

# Parse functions
def next_token_type_is(tokens, type):
    """
    Returns whether the next token type is as specified.

    Args:
        tokens (rply.lexer.LexerStream): LexerStream object containing a line of lexed 
            tokens. This should be a *copy* of the original object, as tokens are 
            discarded once read.
        type (string): String to match token type.
    
    Returns:
        (bool): If the token type matches 'type'.
    """
    return next(tokens).gettokentype() == type


def find_indent_level(tokens):
    """
    Finds the indent level of a line based on the number of INDENT tokens preceding 
    other tokens.

    Args:
        tokens (rply.lexer.LexerStream): LexerStream object containing a line of lexed 
            tokens. This should be a *copy* of the original object, as tokens are 
            discarded once read.
    
    Returns:
        (int): Indent level of the current line. Returns None if line is empty.
    """
    indent_level = 0

    while next_token_type_is(tokens, "INDENT"):
        indent_level += 1

    try:
        next(tokens)
        return indent_level
    except StopIteration:  # no more tokens, i.e. line is empty
        return None


def get_indent_block(initial_indent_level, input, state):
    """
    Returns a list of the code that is within an indentation block, for use in parsing 
    loops and control flow.

    Args:
        initial_indent_level (int): The initial indent level which the code has to 
            return to for the block to be complete.
        input (list): Sliced array containing the lines of code starting with the block.
        state (ast.ParserState): Parser state.
    
    Returns:
        (list): The lines of code within the indentation block.
    """
    indent_block = []
    previous_indent_level = initial_indent_level
    current_indent_level = 0

    for line in input:
        tokens = lexer.lex(line)
        current_indent_level = find_indent_level(copy(tokens))

        # If the current line is empty, let current indent level be equal to the
        # previous indent level
        if current_indent_level is None:
            current_indent_level = previous_indent_level

        if current_indent_level > initial_indent_level:
            # Remove first preceding \t INDENT token and append to repeat block
            # By removing only the first token, code indented once can be run by parse()
            # as if the indent level was 0
            # Code indented more than once is expected to be in a REPEAT loop, so the
            # function is then recursively called again to parse nested loops
            indent_block.append(line.replace("\t", "", 1))
        else:
            # Return the list once current indent level returns to the initial indent level
            return indent_block

        previous_indent_level = current_indent_level

    # Return list if it ends up being the same as the input
    # This occurs for certain scenarios with deeply nested indent-using statements
    return indent_block


def repeat(repeat_count, repeat_indent_level, input, start_lineno, state):
    """
    Performs a REPEAT loop for the parse() function.

    Args:
        repeat_count (int): Number of times to repeat the code block.
        repeat_indent_level (int): The indent level of the preceding REPEAT statement.
        input (list): Sliced array passed from parse(), containing the lines of code 
            after the REPEAT line.
        start_lineno (int): Line number of the first line passed to the function, for 
            error messages.
        state (ast.ParserState): Parser state.
    
    Returns:
        (int): Number of lines within the repeat block, which parse() will have to skip.
    """
    repeat_code_block = get_indent_block(repeat_indent_level, input, state)

    for i in range(repeat_count):
        parse(repeat_code_block, start_lineno, state)

    return len(repeat_code_block)


def repeatuntil(repeat_indent_level, input, start_lineno, state):
    """
    Performs a REPEATUNTIL loop for the parse() function.

    Args:
        repeat_indent_level (int): The indent level of the preceding REPEAT statement.
        input (list): Sliced array passed from parse(), containing the lines of code 
            including and after the REPEAT line.
        start_lineno (int): Line number of the first line passed to the function, for 
            error messages.
        state (ast.ParserState): Parser state.
    
    Returns:
        (int): Number of lines within the repeat block, which parse() will have to skip.
    """
    # Keep tokens within repeat statement for further parsing to check if conditions are met
    repeatuntil_tokens = lexer.lex(input[0])
    # Skip over repeat line
    repeat_code_block = get_indent_block(repeat_indent_level, input[1:], state)

    # Parse REPEATUNTIL condition to gauge if it is satisfied or not
    repeatuntil_condition = parser.parse(copy(repeatuntil_tokens), state=state).eval()
    # Perform loop while condition is not met
    while not repeatuntil_condition.value:  # Check Python bool, not Traversal bool
        parse(repeat_code_block, start_lineno, state)
        repeatuntil_condition = parser.parse(
            copy(repeatuntil_tokens), state=state
        ).eval()

    return len(repeat_code_block)


def if_elseif_else(if_indent_level, input, start_lineno, state):
    """
    Store IF...ELSE IF... ELSE conditional statements before passing to the 
    parse_if_elseif_else() function.

    Args:
        if_indent_level (int): The indent level of the preceding IF statement 
            (and thus ELSE IF and ELSE statements)
        input (list): Sliced array passed from parse(), containing the lines of code 
            including and after the IF line.
        start_lineno (int): Line number of the first line passed to the function, for 
            error messages.
        state (ast.ParserState): Parser state.
    
    Returns:
        (int): Number of lines within the if... else if... else block, which parse() 
            will have to skip. Returned from calling parse_if_eliseif_else().
    """
    # Keep track of number of condition statements to calculate how many lines to skip later on
    conditional_statements_length = 1  # Already found one 'if' statement

    # Setting up storage of 'if' and 'else' information
    if_code_block = []
    else_code_block = []

    # Setting up storage of 'else if' information (there may be multiple 'else if' blocks)
    elseif_pos = []  # Array of all pointers for 'else if' statements
    elseif_tokens = []  # 2D array of all 'else if' statement tokens
    elseif_code_blocks = []  # 2D array of all 'else if' code blocks

    # Storing 'if' information
    if_pos = 0
    if_tokens = lexer.lex(input[if_pos])
    if_code_block = get_indent_block(if_indent_level, input[if_pos + 1 :], state)

    # Next pointer for a conditional statement (either 'else if' or 'else' statement)
    next_pos = if_pos + len(if_code_block) + 1
    try:
        next_tokens = lexer.lex(input[next_pos])
    # End of input list, only parse 'if' statement
    except IndexError:
        return parse_if_elseif_else(
            start_lineno, state, conditional_statements_length, if_tokens, if_code_block
        )

    # Have to check for potentially multiple 'else if' statements
    is_elseif = next_token_type_is(copy(next_tokens), "ELSEIF")
    if is_elseif:
        while is_elseif:
            conditional_statements_length += 1

            # Storing first 'else if' information
            elseif_pos.append(next_pos)
            elseif_tokens.append(next_tokens)
            indent_code_block = get_indent_block(
                if_indent_level, input[next_pos + 1 :], state
            )
            elseif_code_blocks.append(indent_code_block)

            next_pos = next_pos + len(indent_code_block) + 1
            try:
                next_tokens = lexer.lex(input[next_pos])
            # End of input list, only parse up to 'else if' statements added so far
            except IndexError:
                return parse_if_elseif_else(
                    start_lineno,
                    state,
                    conditional_statements_length,
                    if_tokens,
                    if_code_block,
                    elseif_tokens,
                    elseif_code_blocks,
                )

            is_elseif = next_token_type_is(copy(next_tokens), "ELSEIF")

    # Check for 'else' statement
    if next_token_type_is(copy(next_tokens), "ELSE"):
        conditional_statements_length += 1

        # Storing 'else' information
        else_pos, else_tokens = next_pos, next_tokens
        else_code_block = get_indent_block(
            if_indent_level, input[else_pos + 1 :], state
        )

        next_pos = else_pos + len(else_code_block) + 1
        try:
            next_tokens = lexer.lex(input[next_pos])
        # End of input list, parse statements without checking for illegal follow-up statements
        except IndexError:
            return parse_if_elseif_else(
                start_lineno,
                state,
                conditional_statements_length,
                if_tokens,
                if_code_block,
                elseif_tokens,
                elseif_code_blocks,
                else_code_block,
            )

    # Check for illegal follow-up of 'else if' or 'else' after an 'else' statement
    if next_token_type_is(copy(next_tokens), "ELSEIF") or next_token_type_is(
        copy(next_tokens), "ELSE"
    ):
        print(f"On line {start_lineno + next_pos}:", end=" ")
        raise SyntaxError(
            "You cannot follow 'else' with another 'else' or 'else if' statement"
        )

    return parse_if_elseif_else(
        start_lineno,
        state,
        conditional_statements_length,
        if_tokens,
        if_code_block,
        elseif_tokens,
        elseif_code_blocks,
        else_code_block,
    )


def parse_if_elseif_else(
    start_lineno,
    state,
    conditional_statements_length,
    if_tokens,
    if_code_block,
    elseif_tokens=[],
    elseif_code_blocks=[],
    else_code_block=[],
):
    """
    Parse IF...ELSE IF... ELSE conditional statements. Called from the if_elseif_else() 
    function.

    Args:
        start_lineno (int): Line number of the first line passed to the function, for 
            error messages.
        state (ast.ParserState): Parser state.
        conditional_statements_length (int): Number of conditional statements to add to 
            the number of lines skipped.
        if_tokens (rply.lexer.LexerStream): Tokenised IF statement line.
        if_code_block (list): Code block following the IF statement.
        elseif_tokens (list[rply.lexer.LexerStream]): List of tokenised ELSE IF 
            statement lines. Empty by default.
        elseif_code_blocks (list[list]): List of code blocks following each ELSE IF 
            statement. Empty by default.
        else_code_block (list): Code block following the ELSE statement. 
            Empty by default.
   
    Returns:
        (int): Number of lines within the if... else if... else block, which parse() 
            will have to skip.
    """
    # Calculate lines needed to be skipped
    code_block_length = (
        len(if_code_block)
        + sum(len(block) for block in elseif_code_blocks)
        + len(else_code_block)
    )
    lines_skipped = code_block_length + conditional_statements_length - 1

    # Parse if IF condition is satisfied
    if_condition = parser.parse(if_tokens, state=state).eval()
    if if_condition.value:
        parse(if_code_block, start_lineno, state)
        return lines_skipped

    # Check each ELSE IF condition
    for elseif_statement, elseif_code_block in zip(elseif_tokens, elseif_code_blocks):
        elseif_condition = parser.parse(elseif_statement, state=state).eval()
        # Parse if ELSE IF condition is satisfied
        if elseif_condition.value:
            parse(elseif_code_block, start_lineno, state)
            return lines_skipped

    # Parse if ELSE condition is satisfied
    if else_code_block:  # Else statement exists if else_code_block is not empty
        parse(else_code_block, start_lineno, state)
        return lines_skipped

    return lines_skipped


def parse(input, start_lineno, state):
    """
    Parse input from an array of strings.

    Args:
        input (list): Array containing each line of code input.
        start_lineno(int): Line number of the first line passed to the function, for 
            error messages.
        state (ast.ParserState): Parser state.
    """
    repeat_count = 0  # For REPEAT statements
    previous_indent_level = 0
    current_indent_level = 0
    lines_skipped = 0

    for idx, line in enumerate(input):
        tokens = lexer.lex(line)
        lineno = idx + start_lineno
        current_indent_level = find_indent_level(copy(tokens))

        # If the current line is empty, let current indent level be equal to the
        # previous indent level
        if current_indent_level is None:
            current_indent_level = previous_indent_level

        if lines_skipped > 0:
            lines_skipped -= 1
            continue

        # REPEAT statement found
        if next_token_type_is(copy(tokens), "REPEAT"):
            try:
                # Don't .eval() as this returns an int?
                repeat_count = parser.parse(tokens, state=state)
            except:
                print(f"On line {lineno}:", end=" ")
                raise
            lines_skipped = repeat(
                repeat_count, current_indent_level, input[idx + 1 :], lineno + 1, state
            )
        # REPEATUNTIL statement found
        elif next_token_type_is(copy(tokens), "REPEATUNTIL"):
            try:
                parser.parse(tokens, state=state).eval()
            except:
                print(f"On line {lineno}:", end=" ")
                raise
            lines_skipped = repeatuntil(
                current_indent_level, input[idx:], lineno + 1, state
            )
        # IF statement found
        elif next_token_type_is(copy(tokens), "IF"):
            try:
                parser.parse(tokens, state=state).eval()
            except:
                print(f"On line {lineno}:", end=" ")
                raise
            lines_skipped = if_elseif_else(
                current_indent_level, input[idx:], lineno + 1, state
            )
        # Normal statement parsed using RPLY's native parser
        else:
            try:
                parser.parse(tokens, state=state).eval()
            except:
                print(f"On line {lineno}:", end=" ")
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

    # Check start time
    start_time = time.time()
    
    # Open and parse test.trv file by default
    if len(sys.argv) == (1 if sys.argv[1] != "-t" else 2):
        with open("test.trv", "r") as test_input:
            state = ParserState()
            parse(test_input.readlines(), 1, state)
    # Open and parse user-defined file
    elif len(sys.argv) == (2 if sys.argv[1] != "-t" else 3):
        trv_file = sys.argv[1 if sys.argv[1] != "-t" else 2]
        with open(trv_file, "r") as user_input:
            state = ParserState()
            parse(user_input.readlines(), 1, state)
    else:
        raise OSError("Too many command-line arguments!")

    if sys.argv[1] == "-t":
        # Check end time and calculate time elapsed
        end_time = time.time()
        print(f"TIME ELAPSED: {end_time - start_time}")
