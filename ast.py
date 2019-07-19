# State instance which gets passed to parser
class ParserState(object):
    def __init__(self):
        self.variables = {}  # Hold a dict of declared variables


# Integers
class Integer():
    def __init__(self, value):
        self.value = int(value)
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self
    
    def equals(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value == right.value)
        else:
            return Condition(False)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to an integer!")

    def less_than_equals(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value <= right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to an integer using '<='!")
    
    def less_than(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value < right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to an integer using '<'!")

    def greater_than_equals(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value >= right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to an integer using '>='!")
    
    def greater_than(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value > right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to an integer using '>'!")
    
    def add(self, right):
        if type(right) is Integer:
            return Integer(self.value + right.value)
        elif type(right) is Decimal:
            return Decimal(self.value + right.value)
        elif type(right) is Text:
            return Text(str(self.value)+ right.value)
        raise ValueError(f"You cannot add {type(right).__name__.lower()} to an integer!")
    
    def sub(self, right):
        if type(right) is Integer:
            return Integer(self.value - right.value)
        elif type(right) is Decimal:
            return Decimal(self.value - right.value)
        raise ValueError(f"You cannot subtract {type(right).__name__.lower()} from an integer!")
    
    def mul(self, right):
        if type(right) is Integer:
            return Integer(self.value * right.value)
        elif type(right) is Decimal:
            return Decimal(self.value * right.value)
        elif type(right) is Text:
            return Text(self.value * right.value)
        raise ValueError(f"You cannot multiply {type(right).__name__.lower()} with an integer!")
    
    def div(self, right):
        if type(right) is Integer or type(right) is Decimal:  # Always perform true divison
            return Decimal(self.value / right.value)
        raise ValueError(f"You cannot divide {type(right).__name__.lower()} from an integer!")


# Floats
class Decimal():
    def __init__(self, value):
        self.value = float(value)
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self

    def equals(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value == right.value)
        else:
            return Condition(False)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a decimal number!")

    def less_than_equals(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value <= right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a decimal number using '<='!")
    
    def less_than(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value < right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a decimal number using '<'!")

    def greater_than_equals(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value >= right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a decimal number using '>='!")
    
    def greater_than(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Condition(self.value > right.value)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a decimal number using '>'!")
    
    def add(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Decimal(self.value + right.value)
        if type(right) is Text:
            return Text(str(self.value) + right.value)
        raise ValueError(f"You cannot add {type(right).__name__.lower()} to a decimal number!")
    
    def sub(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Decimal(self.value - right.value)
        raise ValueError(f"You cannot subtract {type(right).__name__.lower()} from a decimal number!")
    
    def mul(self, right):
        if type(right) is Integer or type(right) is Decimal:
            return Decimal(self.value * right.value)
        raise ValueError(f"You cannot multiply {type(right).__name__.lower()} with a decimal number!")
    
    def div(self, right):
        if type(right) is Integer or type(right) is Decimal:  # Always perform true divison
            return Decimal(self.value / right.value)
        raise ValueError(f"You cannot divide {type(right).__name__.lower()} from a decimal number!")


# Strings
class Text():
    def __init__(self, value):
        self.value = str(value)
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self

    def equals(self, right):
        if type(right) is Text:
            return Condition(self.value == right.value)
        else:
            return Condition(False)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to text!")

    def less_than_equals(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to text using '<='!")
    
    def less_than(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to text using '<'!")

    def greater_than_equals(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to text using '>='!")
    
    def greater_than(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to text using '>'!")

    def add(self, right):
        if type(right) is Text:
            return Text(self.value + right.value)
        elif type(right) is Integer or type(right) is Decimal:
            return Text(self.value + str(right.value))
        elif type(right) is Condition:
            return Text(self.value + str(right.value).lower())  # Booleans are in lower case
        raise ValueError(f"You cannot add {type(right).__name__.lower()} to text!")
    
    def sub(self, right):
        raise ValueError("You cannot subtract text!")
    
    def mul(self, right):
        if type(right) is Integer:
            return Text(self.value * right.value)
        raise ValueError(f"You cannot multiply text with {type(right).__name__.lower()}!")
    
    def div(self, right):
        raise ValueError("You cannot divide text!")


# Booleans
class Condition():
    def __init__(self, value):
        self.value = bool(value)
    
    def __repr__(self):
        return str(self.value).lower()
    
    def eval(self):
        return self

    def equals(self, right):
        if type(right) is Condition:
            return Condition(self.value == right.value)
        else:
            return Condition(False)
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a condition!")

    def less_than_equals(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a condition using '<='!")
    
    def less_than(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a condition using '<'!")

    def greater_than_equals(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a condition using '>='!")
    
    def greater_than(self, right):
        raise ValueError(f"You cannot compare {type(right).__name__.lower()} to a condition using '>'!")
    
    def add(self, right):
        raise ValueError("You cannot add anything to a condition!")
    
    def sub(self, right):
        raise ValueError("You cannot subtract anything from a condition!")
    
    def mul(self, right):
        raise ValueError("You cannot multiply anything with a condition!")
    
    def div(self, right):
        raise ValueError("You cannot divide anything from a condition!")


# Binary operators
class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Equals(BinaryOp):
    def eval(self):
        result = self.left.eval().equals(self.right.eval())
        return result


class NotEquals(BinaryOp):
    def eval(self):
        result = self.left.eval().equals(self.right.eval())
        result.value = not result.value  # Invert boolean value of Condition object
        return result  # Returns a Condition object, not a boolean (returning 'not result' would be a boolean)


class LessThanEquals(BinaryOp):
    def eval(self):
        return self.left.eval().less_than_equals(self.right.eval())


class LessThan(BinaryOp):
    def eval(self):
        return self.left.eval().less_than(self.right.eval())


class GreaterThanEquals(BinaryOp):
    def eval(self):
        return self.left.eval().greater_than_equals(self.right.eval())


class GreaterThan(BinaryOp):
    def eval(self):
        return self.left.eval().greater_than(self.right.eval())


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


# Unary operators
class UnaryOp():
    def __init__(self, value):
        self.value = value


class UnaryAdd(UnaryOp):
    def eval(self):
        return self.value.eval().mul(Integer(1))


class UnarySub(UnaryOp):
    def eval(self):
        return self.value.eval().mul(Integer(-1))


# Print
class Output():
    def __init__(self, value):
        self.value = value
    
    def eval(self):
        print(self.value.eval())


# Variables
class Variable():
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
    def eval(self):
        return self.value.eval()

# Empty line
class EmptyLine():
    def eval(self):
        return None