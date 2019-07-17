from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()
    
    def _add_tokens(self):
        # Output/print
        self.lexer.add('OUTPUT', r'output|print')
        # Operators
        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        # Numbers
        self.lexer.add('FLOAT', r'\d+\.\d+')  # Precedence applies so check for floats before integers which would otherwise match
        self.lexer.add('INTEGER', r'\d+')
        # Parentheses
        self.lexer.add('LPAREN', r'\(')
        self.lexer.add('RPAREN', r'\)')
        # Ignore all whitespace characters
        self.lexer.ignore(r'\s+')
    
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
