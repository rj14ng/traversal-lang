from rply import ParserGenerator
from ast import Number, Add, Sub, Mul, Div, Output

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser
            ['OUTPUT', 'NEWLINE', 'ADD', 'SUB', 'MUL', 'DIV', 'NUMBER'], 
            # A list of precedence rules
            precedence = [
                ('left', ['ADD', 'SUB']),
                ('left', ['MUL', 'DIV'])
            ]
        )
    
    def parse(self):
        @self.pg.production("program : OUTPUT expression NEWLINE")
        def program(p):
            return Output(p[1])
        
        @self.pg.production("expression : expression ADD expression")
        @self.pg.production("expression : expression SUB expression")
        @self.pg.production("expression : expression MUL expression")
        @self.pg.production("expression : expression DIV expression")
        def expression(p):
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
        
        @self.pg.production("expression : NUMBER")
        def number(p):
            return Number(p[0].value)
        
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)
    
    def get_parser(self):
        return self.pg.build()