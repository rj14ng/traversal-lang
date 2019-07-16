from rply import ParserGenerator
from ast import Integer, Float, Add, Sub, Mul, Div, Output

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser
            ['OUTPUT', 'ADD', 'SUB', 'MUL', 'DIV', 'INTEGER', 'FLOAT'], 
            # A list of precedence rules
            precedence = [
                ('left', ['ADD', 'SUB']),
                ('left', ['MUL', 'DIV'])
            ]
        )
    
    def parse(self):
        @self.pg.production("statement : OUTPUT expression")
        def statement_output(p):
            return Output(p[1])
        
        @self.pg.production("expression : expression ADD expression")
        @self.pg.production("expression : expression SUB expression")
        @self.pg.production("expression : expression MUL expression")
        @self.pg.production("expression : expression DIV expression")
        def expression_binop(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'ADD':
                return Add(left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(left, right)
            elif operator.gettokentype() == 'MUL':
                return Mul(left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(left, right)
        
        @self.pg.production("expression : INTEGER")
        def expr_int(p):
            return Integer(int(p[0].getstr()))
        
        @self.pg.production("expression : FLOAT")
        def expr_float(p):
            return Float(float(p[0].getstr()))
        
        @self.pg.error
        def error_handle(token):
            # Error message for those pesky '$end' tokens
            # Is this needed anymore now that NEWLINE tokens don't exist anymore?
            if token.gettokentype() == "$end":
                raise ValueError("Ran into a $end token where it wasn't expected. Maybe you missed a newline somewhere?")
            # Generic error message
            raise ValueError(f"Ran into a {token.gettokentype()} token where it wasn't expected.")
    
    def get_parser(self):
        return self.pg.build()
