# Token types
INTEGER = 'INTEGER'
PLUS    = 'PLUS'
MINUS   = 'MINUS'
EOF     = 'EOF'  # end-of-file, no more input left for lexical analysis

class Token(object):
    def __init__(self, type, value):
        # Token type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        # Token value: non-negative integer, '+', '-', or None
        self.value = value
    
    def __str__(self):
        '''
        String representation of the class instance.

        Examples:
        Token(INTEGER, 3)
        Token(PLUS, '+')
        '''
        return f"Token({self.type}, {repr(self.value)})"
    
    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        # String input, e.g. "3 + 5" or "12 - 5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # Current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception("Error parsing input")  # might come back one day to make this error message more user friendly
    
    def advance(self):
        '''
        Advance the position pointer and set the 'current_char' variable.
        '''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        '''
        Return a (multidigit) integer consumed from the input.
        '''
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        '''
        Lexical analyser (also known as lexer or tokeniser)

        This method is responsible for breaking a sentence into tokens, one at a time.
        '''
        while self.current_char is not None:

            # Skip whitespace characters
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Return INTEGER tokens
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            # Return PLUS token
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            # Return MINUS token
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            # Raise an exception if character is anything else
            self.error
        
        return Token(EOF, None)
    
    def eat(self, token_type):
        # Compare the current token type with the passed token type
        # If they match, 'eat' the current token then assign the next token to self.current_token
        # Otherwise raise an exception
        # This will make more sense after reading the code for the expr() function below
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        '''
        Parser / Interpreter

        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        '''
        # Set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # Expect the current token to be an integer
        left = self.current_token
        self.eat(INTEGER)

        # Expect the current token to either a '+' or '-' symbol
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        # Expect the current token to be an integer
        right = self.current_token
        self.eat(INTEGER)
        # After above call self.current is set to EOF token

        # At this point INTEGER PLUS/MINUS INTEGER sequence of tokens has been successfully found
        # Method can just return result of adding/subtracting the two integers
        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result

def main():
    while True:
        try:
            text = input("calculate> ")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == "__main__":
    main()