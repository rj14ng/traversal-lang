# Token types
INTEGER = 'INTEGER'
ADD     = 'ADD'
SUB     = 'SUB'
MUL     = 'MUL'
DIV     = 'DIV'
LPAREN  = '('
RPAREN  = ')'
EOF     = 'EOF'  # end-of-file, no more input left for lexical analysis


class Token(object):
    def __init__(self, type, value):
        # Token type
        self.type = type
        # Token value
        self.value = value
    
    def __str__(self):
        '''
        String representation of the class instance.

        Examples:
        Token(INTEGER, 3)
        Token(ADD, '+')
        Token(MUL, '*')
        '''
        return f"Token({self.type}, {repr(self.value)})"
    
    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # String input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0

        self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception("Invalid character")  # might come back one day to make this error message more user friendly

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
            
            # Return ADD token
            if self.current_char == '+':
                self.advance()
                return Token(ADD, '+')
            
            # Return SUB token
            if self.current_char == '-':
                self.advance()
                return Token(SUB, '-')
            
            # Return MUL token
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            # Return DIV token
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            # Return LPAREN token
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            # Return RPAREN token
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            # Raise an exception if character is anything else
            self.error()
        
        return Token(EOF, None)
