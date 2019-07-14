from lexer import *

class AST(object):
    '''
    Abstract syntax tree.
    '''
    pass


class BinOp(AST):
    '''
    Binary operators.
    '''
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    '''
    Holds an INTEGER token and its value.
    '''
    def __init__(self, token):
        self.token = token
        self.value = token.value


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
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
    
    def term(self):
        '''
        term : factor ((MUL | DIV) factor)*
        '''
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            if token.type == DIV:
                self.eat(DIV)
            
            node = BinOp(left=node, op=token, right=self.factor())
        
        return node
    
    def expr(self):
        '''
        Arithmetic expression parser

        Grammar:
        expr   : term ((ADD | SUB) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        '''

        node = self.term()

        while self.current_token.type in (ADD, SUB):
            token = self.current_token
            if token.type == ADD:
                self.eat(ADD)
            elif token.type == SUB:
                self.eat(SUB)
            
            node = BinOp(left=node, op=token, right=self.term())
        
        return node
    
    def parse(self):
        node = self.expr()
        if self.current_token.type != EOF:
            self.error()  # Throw an error if there are unconsumed tokens left
        return node
