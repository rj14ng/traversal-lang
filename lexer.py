from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()
    
    def _add_tokens(self):
        # String AKA text
        self.lexer.add('TEXT', '(""".*?""")|(".*?")|(\'.*?\')')  # Strings denoted by """string""", "string", and 'string'
        # Numbers (float AKA decimal, integer)
        self.lexer.add('DECIMAL', r'\d+\.\d+')  # (Precedence - floats before integers which would otherwise match)
        self.lexer.add('INTEGER', r'\d+')
        # Output/print
        self.lexer.add('OUTPUT', r'output|print')
        # Boolean AKA condition
        self.lexer.add('CONDITION', r'(?i)true|false')  # Case insensitive
        # Operators
        self.lexer.add('ADD', r'\+')
        self.lexer.add('SUB', r'-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        # Equals acts as assignment (=) and equality (==) operator
        self.lexer.add('EQUALS', r'=')
        # Not equals acts as != operator
        self.lexer.add('NOTEQUALS', r'not=')
        # Variables
        self.lexer.add('VARIABLE', '[a-zA-Z_][a-zA-Z0-9_]*')  # (Precedence - put all keywords before variable names which would otherwise match)
        # Parentheses
        self.lexer.add('LPAREN', r'\(')
        self.lexer.add('RPAREN', r'\)')
        # Ignore all whitespace characters
        self.lexer.ignore(r'\s+')
    
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
