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
            self.error
        
        return Token(EOF, None)


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # Set current token to the first token taken from input
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception("Invalid syntax")  # might come back one day to make this error message more user friendly

    def eat(self, token_type):
        # Compare the current token type with the passed token type
        # If they match, 'eat' the current token then assign the next token to self.current_token
        # Otherwise raise an exception
        # This will make more sense after reading the code for the expr() function below
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        '''
        factor : INTEGER | LPAREN expr RPAREN
        '''
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()  # Recursively use expr() method within parentheses
            self.eat(RPAREN)
            return result
    
    def term(self):
        '''
        term : factor ((MUL | DIV) factor)*
        '''
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            if token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        
        return result
    
    def expr(self):
        '''
        Arithmetic expression parser

        Grammar:
        expr   : term ((ADD | SUB) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        '''

        result = self.term()

        while self.current_token.type in (ADD, SUB):
            token = self.current_token
            if token.type == ADD:
                self.eat(ADD)
                result += self.term()
            elif token.type == SUB:
                self.eat(SUB)
                result -= self.term()
        
        return result

def main():
    while True:
        try:
            text = input("calculate> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.expr()
        print(result)

if __name__ == "__main__":
    main()