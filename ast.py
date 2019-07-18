class ParserState(object):  # State instance which gets passed to parser
    def __init__(self):
        self.variables = {}  # Hold a dict of declared variables

class Integer():
    def __init__(self, value):
        self.value = int(value)
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self
    
    def add(self, right):
        if type(right) is Integer:
            return Integer(self.value + right.value)
        if type(right) is Float:
            return Float(self.value + right.value)
        raise ValueError("You cannot add that to an integer!")
    
    def sub(self, right):
        if type(right) is Integer:
            return Integer(self.value - right.value)
        if type(right) is Float:
            return Float(self.value - right.value)
        raise ValueError("You cannot subtract that from an integer!")
    
    def mul(self, right):
        if type(right) is Integer:
            return Integer(self.value * right.value)
        if type(right) is Float:
            return Float(self.value * right.value)
        raise ValueError("You cannot multiply that with an integer!")
    
    def div(self, right):
        if type(right) is Integer or type(right) is Float:  # Always perform true divison
            return Float(self.value / right.value)
        raise ValueError("You cannot divide that from an integer!")


class Float():
    def __init__(self, value):
        self.value = float(value)
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self
    
    def add(self, right):
        if type(right) is Integer or type(right) is Float:
            return Float(self.value + right.value)
        raise ValueError("You cannot add that to a decimal number!")
    
    def sub(self, right):
        if type(right) is Integer or type(right) is Float:
            return Float(self.value - right.value)
        raise ValueError("You cannot subtract that from a decimal number!")
    
    def mul(self, right):
        if type(right) is Integer or type(right) is Float:
            return Float(self.value * right.value)
        raise ValueError("You cannot multiply that with a decimal number!")
    
    def div(self, right):
        if type(right) is Integer or type(right) is Float:  # Always perform true divison
            return Float(self.value / right.value)
        raise ValueError("You cannot divide that from a decimal number!")


class String():
    def __init__(self, value):
        self.value = str(value)
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self

    def add(self, right):
        if type(right) is String:  # Can only add strings to strings
            return String(self.value + right.value)
        raise ValueError("You cannot add that to text!")
    
    def sub(self, right):
        raise ValueError("You cannot subtract text!")
    
    def mul(self, right):
        raise ValueError("You cannot multiply text!")
    
    def div(self, right):
        raise ValueError("You cannot divide text!")


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        return self.left.eval().add(self.right.eval())


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval().sub(self.right.eval())


class Mul(BinaryOp):
    def eval(self):
        return self.left.eval().mul(self.right.eval())


class Div(BinaryOp):
    def eval(self):
        return self.left.eval().div(self.right.eval())


class UnaryOp():
    def __init__(self, value):
        self.value = value


class UnaryAdd(UnaryOp):
    def eval(self):
        return self.value.eval().mul(Integer(1))


class UnarySub(UnaryOp):
    def eval(self):
        return self.value.eval().mul(Integer(-1))


class Output():
    def __init__(self, value):
        self.value = value
    
    def eval(self):
        print(self.value.eval())


class Variable():
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self.value.eval()