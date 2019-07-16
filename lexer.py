from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()
    
    def _add_tokens(self):
        # Output
        self.lexer.add('OUTPUT', r'output')
        # Newline
        self.lexer.add('NEWLINE', r'\n')
        # Operators
        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        # Numbers
        self.lexer.add('FLOAT', r'\d+\.\d+')  # Check for float before integer!
        self.lexer.add('INTEGER', r'\d+')
        # Ignore all whitespace characters except for newline
        self.lexer.ignore('[ \t\r\f\v]+')
    
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
