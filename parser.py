from rply import ParserGenerator
from ast import *

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser
            ['OUTPUT', 'VARIABLE', 'ADD', 'SUB', 'MUL', 'DIV', 'EQUALS', 'FLOAT', 'INTEGER', 'LPAREN', 'RPAREN'], 
            # A list of precedence rules with ascending precedence, to disambiguate ambiguous production rules
            precedence = [
                ('left', ['ADD', 'SUB']),
                ('left', ['MUL', 'DIV'])
            ]
        )
    
    def parse(self):
        @self.pg.production("statement : OUTPUT expression")
        def statement_output(state, p):
            return Output(p[1])
        
        @self.pg.production("statement : VARIABLE EQUALS expression")
        def statement_assignment(state, p):
            # Currently variables are immutable - can only assign if it doesn't exist yet
            if state.variables.get(p[0].getstr(), None) is None:
                state.variables[p[0].getstr()] = p[2].eval()
                return p[2]
            
            # Otherwise raise error
            raise ValueError(f"Variable {p[0].getstr()} is already defined.")
        
        @self.pg.production("expression : LPAREN expression RPAREN")
        def expr_paren(state, p):
            return p[1]
        
        @self.pg.production("expression : expression ADD expression")
        @self.pg.production("expression : expression SUB expression")
        @self.pg.production("expression : expression MUL expression")
        @self.pg.production("expression : expression DIV expression")
        def expression_binop(state, p):
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
            else:
                raise AssertionError("This should not be possible!")
        
        @self.pg.production("expression : ADD expression")
        @self.pg.production("expression : SUB expression")
        def expression_unaryop(state, p):
            operator = p[0]
            if operator.gettokentype() == 'ADD':
                return UnaryAdd(p[1])
            elif operator.gettokentype() == 'SUB':
                return UnarySub(p[1])
            else:
                raise AssertionError("This should not be possible!")
        
        @self.pg.production("expression : INTEGER")
        def expr_int(state, p):
            return Integer(int(p[0].getstr()))
        
        @self.pg.production("expression : FLOAT")
        def expr_float(state, p):
            return Float(float(p[0].getstr()))

        @self.pg.production("expression : VARIABLE")
        def expr_variable(state, p):
            # Cannot return value of a variable if it isn't defined
            if state.variables.get(p[0].getstr(), None) is None:
                raise ValueError(f"Variable {p[0].getstr()} is not yet defined.")
            
            # Otherwise return value
            return Variable(state.variables[p[0].getstr()])

        @self.pg.error
        def error_handle(state, token):
            # Generic error message
            raise ValueError(f"Ran into a {token.gettokentype()} token where it wasn't expected.")
    
    def get_parser(self):
        return self.pg.build()
