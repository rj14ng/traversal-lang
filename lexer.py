from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # NB - All keywords must include (?!\w) in regex so they don't match if other
        # characters appear afterwards

        # String AKA text
        # Strings denoted by """string""", "string", and 'string'
        self.lexer.add("TEXT", '(""".*?""")|(".*?")|(\'.*?\')')
        # Numbers (float AKA decimal, integer)
        # (Precedence - floats before integers which would otherwise match)
        self.lexer.add("DECIMAL", r"\d+\.\d+")
        self.lexer.add("INTEGER", r"\d+")
        # Output/print
        self.lexer.add("OUTPUT", r"output(?!\w)|print(?!\w)|say(?!\w)")
        # Boolean AKA condition
        self.lexer.add("CONDITION", r"(?i)true(?!\w)|false(?!\w)")  # Case insensitive
        # Comments
        self.lexer.ignore(r"//.*")  # Matches // and all following characters
        # Operators
        self.lexer.add("ADD", r"\+")
        self.lexer.add("SUB", r"-")
        self.lexer.add("MUL", r"\*")
        self.lexer.add("DIV", r"/")
        self.lexer.add("POW", r"\^")
        self.lexer.add("MOD", r"mod(?!\w)")
        # Equals acts as assignment (=) and equality (==) operator
        self.lexer.add("=", r"=")
        # Not equals acts as != operator
        self.lexer.add("NOT=", r"not=")
        # Comparison operators
        self.lexer.add("<=", r"<=")
        self.lexer.add("<", r"<")
        self.lexer.add(">=", r">=")
        self.lexer.add(">", r">")
        # Logical operators
        self.lexer.add("AND", r"and")
        self.lexer.add("OR", r"or")
        self.lexer.add("NOT", r"not")
        # Loops
        self.lexer.add("REPEATUNTIL", r"repeat until(?!\w)")
        self.lexer.add("REPEAT", r"repeat(?!\w)")
        # Conditional statements
        self.lexer.add("IF", r"if(?!\w)")
        self.lexer.add("ELSEIF", r"(else if)(?!\w)|(but if)(?!\w)|(otherwise if)(?!\w)")
        self.lexer.add("ELSE", r"else(?!\w)|otherwise(?!\w)")
        # Variables
        # (Precedence - put all keywords before variable names which would otherwise match)
        self.lexer.add("VARIABLE", "[a-zA-Z_][a-zA-Z0-9_]*")
        # Parentheses
        self.lexer.add("LPAREN", r"\(")
        self.lexer.add("RPAREN", r"\)")
        # Indents
        self.lexer.add("INDENT", r"\t")
        # Newlines
        self.lexer.add("NEWLINE", r"\n")
        # Ignore all other whitespace characters
        self.lexer.ignore(r"[ \r\f\v]+")

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
