# Token types
INTEGER = 'INTEGER'
PLUS    = 'PLUS'
EOF     = 'EOF'  # end-of-file, no more input left for lexical analysis

class Token(object):
    def __init__(self, type, value):
        # Token type: INTEGER, PLUS, or EOF
        self.type = type
        # Token value: 0-9, '+', or None
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
        # String input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # Current token instance
        self.current_token = None
    
    def error(self):
        raise Exception("Error parsing input")  # might come back one day to make this error message more user friendly
    
    def get_next_token(self):
        '''
        Lexical analyser (also known as lexer or tokeniser)

        This method is responsible for breaking a sentence into tokens, one at a time.
        '''
        text = self.text

        # Return EOF token if position index is past the end of the text
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        
        # Get a character at the current position and decide what token to create based on the single character
        current_char = text[self.pos]

        # Return INTEGER token if character is a digit, then increment position index by 1
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        # Return PLUS token if character is '+', then increment position index by 1
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        
        # Raise an exception if character is anything else
        self.error
    
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
        expr -> INTEGER PLUS INTEGER
        '''
        # Set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # Expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # Expect the current token to a '+' symbol
        op = self.current_token
        self.eat(PLUS)

        # Expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        # After above call self.current is set to EOF token

        # At this point INTEGER PLUS INTEGER sequence of tokens has been successfully found
        # Method can just return result of adding the two integers
        result = left.value + right.value
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