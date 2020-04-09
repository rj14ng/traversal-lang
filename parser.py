from rply import ParserGenerator
from ast import *

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser
            # INDENT not added as it's not actually used within RPLY's native parser functions
            ['TEXT', 'DECIMAL', 'INTEGER', 'OUTPUT', 'CONDITION', 'REPEATUNTIL', 'REPEAT', 'IF', 'ELSEIF', 'ELSE', 'VARIABLE',
             'ADD', 'SUB', 'MUL', 'DIV', '=', 'NOT=', '<=', '<', '>=', '>', 'AND', 'OR', 'NOT',
             'LPAREN', 'RPAREN', 'NEWLINE', '$end'],
            # A list of precedence rules with ascending precedence, to disambiguate ambiguous production rules
            precedence = [
                ('left', ['AND', 'OR']),
                ('left', ['NOT']),
                ('left', ['=', 'NOT=', '<=', '<', '>=', '>']),
                ('left', ['ADD', 'SUB']),
                ('left', ['MUL', 'DIV']),
            ]
        )
    
    def parse(self):
        @self.pg.production("statement : statement NEWLINE")
        def statement_newline(state, p):
            return p[0]
        
        @self.pg.production("statement : OUTPUT expression")
        def statement_output(state, p):
            return Output(p[1])
        
        @self.pg.production("statement : VARIABLE = expression")
        def statement_assignment(state, p):
            state.variables[p[0].getstr()] = p[2].eval()
            return p[2]
        
        @self.pg.production("statement : IF expression")
        @self.pg.production("statement : ELSEIF expression")
        def statement_if_elseif(state, p):
            expr = p[1].eval()
            if type(expr) is not Condition:
                raise AssertionError("You must follow 'if', 'else if', and/or 'else' with a condition")
            return expr
        
        @self.pg.production("statement : ELSE")
        def statement_else(state, p):
            return DoNothing()

        @self.pg.production("statement : REPEATUNTIL expression")
        def statement_repeat_until(state, p):
            expr = p[1].eval()
            if type(expr) is not Condition:
                raise AssertionError("You must follow 'repeat until' with a condition")
            return expr

        @self.pg.production("statement : REPEAT expression")
        def statement_repeat(state, p):
            expr = p[1].eval()
            if type(expr) is not Integer:
                raise AssertionError("You must follow 'repeat' with an integer")

            repeat_count = expr.value
            if repeat_count <= 0:
                raise AssertionError("You must repeat 1 or more times")
            return repeat_count
        
        @self.pg.production("terminator : $end")
        @self.pg.production("statement : terminator")
        @self.pg.production("statement : NEWLINE")
        # Ignore empty and commented lines
        def statement_empty(state, p):
            return DoNothing()
        
        @self.pg.production("expression : LPAREN expression RPAREN")
        def expression_paren(state, p):
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
        
        @self.pg.production("expression : expression = expression")
        @self.pg.production("expression : expression NOT= expression")
        @self.pg.production("expression : expression <= expression")
        @self.pg.production("expression : expression < expression")
        @self.pg.production("expression : expression >= expression")
        @self.pg.production("expression : expression > expression")
        def expression_equality(state, p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == '=':
                return Equals(left, right)
            elif operator.gettokentype() == 'NOT=':
                return NotEquals(left, right)
            elif operator.gettokentype() == '<=':
                return LessThanEquals(left, right)
            elif operator.gettokentype() == '<':
                return LessThan(left, right)
            elif operator.gettokentype() == '>=':
                return GreaterThanEquals(left, right)
            elif operator.gettokentype() == '>':
                return GreaterThan(left, right)
            else:
                raise AssertionError("This should not be possible!")
        
        @self.pg.production("expression : expression AND expression")
        @self.pg.production("expression : expression OR expression")
        def expression_and_or(state, p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'AND':
                return And(left, right)
            elif operator.gettokentype() == 'OR':
                return Or(left, right)
            else:
                raise AssertionError("This should not be possible!")
        
        @self.pg.production("expression : NOT expression")
        def expression_not(state, p):
            return Not(p[1])
        
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
        def expression_integer(state, p):
            return Integer(int(p[0].getstr()))
        
        @self.pg.production("expression : DECIMAL")
        def expression_decimal(state, p):
            return Decimal(float(p[0].getstr()))
        
        @self.pg.production("expression : TEXT")
        def expression_text(state, p):
            return Text(p[0].getstr().strip('"\''))  # Strip " or '
        
        @self.pg.production("expression : CONDITION")
        def expression_condition(state, p):
            return Condition(True if p[0].getstr().lower() == "true" else False)

        @self.pg.production("expression : VARIABLE")
        def expression_variable(state, p):
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
