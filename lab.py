"""
6.1010 Spring '23 Lab 10: Symbolic Algebra
"""

import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    """
    Our base class; all other classes we create will 
    inherit from this class.
    Any behaviour that is common between all expressions 
    implemented here.
    """
    precedence = 0
    right_parens = False
    left_parens = False

    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        return Div(other, self)

    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return Pow(other, self)

    def eval(self, mapping):
        """
        For any symbolic expression sym, 
        sym.eval(mapping) will find a numerical value - a float or an int
        (not an instance of Num) for the given expression
        
        Mapping is a dict mapping variable names to values.
        """
        if self.operand == "+":
            return self.left.eval(mapping) + self.right.eval(mapping)
        elif self.operand == "-":
            return self.left.eval(mapping) - self.right.eval(mapping)
        elif self.operand == "*":
            return self.left.eval(mapping) * self.right.eval(mapping)
        elif self.operand == "/":  # /
            return self.left.eval(mapping) / self.right.eval(mapping)
        elif self.operand == "**":  # /
            return self.left.eval(mapping) ** self.right.eval(mapping)

    def simplify(self):
        return self  # var and num the same


class Var(Symbol):
    """
    Instances of Var represent variables (such as 'x', 'y')
    """
    precedence = 3

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"

    def eval(self, mapping):  # base case
        if self.name not in mapping:
            raise NameError

        return mapping[self.name]

    def __eq__(self, other):
        if (
            isinstance(self, type(other)) and self.name == other.name
        ):  # check same class and contents
            return True
        return False

    def deriv(self, item):
        if self.name == item:  # base case 1
            return Num(1)
        return Num(0)


class Num(Symbol):
    """
    Instances of Num represent numbers within symbolic expressions.
    """
    precedence = 3

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"

    def eval(self, mapping):  # base case iof eval
        return self.n

    def __eq__(self, other):
        if isinstance(self, type(other)) and self.n == other.n:
            return True
        return False

    def deriv(self, item):
        return Num(0)  # base case 2


# subclass of Symbol
class BinOp(Symbol):
    """
    Represent a binary operation.
    It is a type of symbolic expression, BinOp should be a subclass of Symbol
    """
    precedence = 0
    right_parens = False
    left_parens = False

    def __init__(self, left, right):
        """
        Initialiser.  Store two instance variables,
        left = a Symbol instance the rep left-hand operation,
        right = a Symbol instance the rep right-hand operation
        """
        if isinstance(left, (int, float)):  # left
            self.left = Num(left)
        elif isinstance(left, str):
            self.left = Var(left)
        else:
            self.left = left

        if isinstance(right, (int,float)):  # right
            self.right = Num(right)
        elif isinstance(right, str):
            self.right = Var(right)
        else:
            self.right = right

    def __str__(self):
        # compare precendences to initial bin operation
        # edge case - e.g. x-y-z is diff to x-(y-z)

        # original_operands = ["+", "-", "*", "/"]
        # if self.operand in original_operands:
        if (
            self.left.precedence < self.precedence
            or self.left_parens
            and self.left.precedence <= self.precedence
        ):  # for Pow
            wrap_left = "(" + str(self.left) + ")"

        else:
            wrap_left = str(self.left)

        if self.right.precedence < self.precedence or (
            self.right_parens and self.right.precedence == self.precedence
        ):
            wrap_right = "(" + str(self.right) + ")"
        else:
            wrap_right = str(self.right)


        return wrap_left + " " + self.operand + " " + wrap_right

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"

    def __eq__(self, other):
        if (
            isinstance(self, type(other))
            and self.left == other.left
            and self.right == other.right
        ):
            return True
        return False


# subclasses of BinOp
class Add(BinOp):
    """
    Addition:
    E1 + E2 results in an instance Add(E1, E2)
    """
    operand = "+"
    precedence = 1
    right_parens = False
    left_parens = False

    def deriv(self, item):
        return Add(self.left.deriv(item), self.right.deriv(item))

    def simplify(self):  # always returns symbol
        simplified_left = self.left.simplify()
        simplified_right = self.right.simplify()

        if isinstance(simplified_left, Num) and isinstance(
            simplified_right, Num
        ):  # add numbers
            return Num(simplified_left.n + simplified_right.n)  # symbol

        if simplified_left == Num(0):  # if add 0
            return simplified_right

        if simplified_right == Num(0):
            return simplified_left

        return Add(simplified_left, simplified_right)


class Sub(BinOp):
    """
    Subtraction:
    E1 - E2 results in an instance Sub(E1, E2)
    """
    operand = "-"
    precedence = 1
    right_parens = True
    left_parens = False

    def deriv(self, item):
        return Sub(self.left.deriv(item), self.right.deriv(item))

    def simplify(self):
        simplified_left = self.left.simplify()
        simplified_right = self.right.simplify()

        if isinstance(simplified_left, Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n - simplified_right.n)

        if simplified_right == Num(0):  # only simplifies on right not 0-x
            return simplified_left

        return Sub(simplified_left, simplified_right)


class Mul(BinOp):
    """
    Multiplication:
    E1 * E2 results in an instance Mul(E1, E2)
    """
    operand = "*"
    precedence = 2
    right_parens = False
    left_parens = False

    def deriv(self, item):
        return Add(
            Mul(self.left, self.right.deriv(item)),
            Mul(self.right, self.left.deriv(item)),
        )

    def simplify(self):
        simplified_left = self.left.simplify()
        simplified_right = self.right.simplify()

        if isinstance(simplified_left, Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n * simplified_right.n)

        if simplified_left == Num(1):  # mul by 1
            return simplified_right
        if simplified_right == Num(1):
            return simplified_left

        if simplified_left == Num(0) or simplified_right == Num(0):  # mul by 0
            return Num(0)

        return Mul(simplified_left, simplified_right)


class Div(BinOp):
    """
    Division:
    E1 / E2 results in an instance Div(E1, E2)
    """
    operand = "/"
    precedence = 2
    right_parens = True
    left_parens = False

    def deriv(self, item):
        return (
            Sub(
                Mul(self.right, self.left.deriv(item)),
                Mul(self.left, self.right.deriv(item)),
            )
        ) / Mul(
            self.right, self.right
        )  # square

    def simplify(self):
        simplified_left = self.left.simplify()
        simplified_right = self.right.simplify()

        if isinstance(simplified_left, Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n / simplified_right.n)

        if simplified_right == Num(1):  # div by 1
            return simplified_left

        if simplified_left == Num(0):  # div by 0
            return Num(0)

        return Div(simplified_left, simplified_right)


class Pow(BinOp):
    """
    Exponentiation:
    E1 ** E2 results in an instance Pow(E1, E2)
    """
    operand = "**"
    precedence = 2
    right_parens = False
    left_parens = True

    def deriv(self, item):
        if isinstance(self.right, Num):
            return Mul(
                Mul(self.right, Pow(self.left, self.right - 1)), self.left.deriv(item)
            )
        raise TypeError

    def simplify(self):
        simplified_left = self.left.simplify()
        simplified_right = self.right.simplify()

        if isinstance(simplified_left, Num) and isinstance(simplified_right, Num):
            return Num(simplified_left.n**simplified_right.n)

        if simplified_right == Num(0):
            return Num(1)

        if simplified_right == Num(1):
            return simplified_left

        if simplified_left == Num(0):
            return simplified_left

        return Pow(simplified_left, simplified_right)


def tokenize(statement):
    """
    Take a string as an input and
    output a list of meaningful tokens 
    (parentheses, variable names, numbers, or operands).
    """
    statement_lst = []

    indx = 0
    while indx != len(statement):  # not
        # indx = 0
        item = statement[indx]

        if item == " ":
            indx += 1
            continue
        elif item in "()":
            indx += 1
            statement_lst.append(item)
        else:
            buffer = ""
            while indx != len(statement) and statement[indx] not in "( )":

                item = statement[indx]
                print(item)
                buffer += item

                indx += 1
            print(buffer)
            statement_lst.append(buffer)
    return statement_lst


 


def parse(tokens):
    """
    Take the output of tokenize and
    return an appropriate instance of Symbol
    """

    def parse_expression(index):
        """
        Takes an integer indexing into the tokens list and
        returns a pair of values
        """
        current = tokens[index]

        # recursive case
        if current == "(":
            expression_1, operand_index = parse_expression(index + 1)  # parse next expression
            expression_2, close_paren_index = parse_expression(operand_index + 1)

            return find_class(tokens[operand_index])(expression_1, expression_2), close_paren_index + 1

        # base cases
        else:
            try:
                return Num(float(current)), index + 1
            except:
                return Var(current), index + 1

    #

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression


def expression(statement):
    """ 
    Parsing strings into symbolic expressions
    """
    return parse(tokenize(statement))


if __name__ == "__main__":
    doctest.testmod()
    # z = Add(Var('x'), Sub(Var('y'), Num(2)))
    # print(repr(z))

    # a = Num(4)
    # b = Num(4)
    # print(a == b)        # False
    # print(a == Num(4.0)) # False
    # print(a == a)        # True
    # print(4 == 4.0)      # True

    # print(tokenize("(x * (-205 - -3))"))
    # print(tokenize("()"))
    # ['(', 'x', '*', '(', '2', '+', '3', ')', ')']

    # print(Pow(2, Var("x")))
    # # 2 ** x

    # print(Pow(Add(Var("x"), Var("y")), Num(1)))
    # # (x + y) ** 1

    # print(Pow(Num(2), Pow(Num(3), Num(4))))
    # # 2 ** 3 ** 4

    # print(Pow(Num(2), Add(Num(3), Num(4))))
    # # 2 ** (3 + 4)

    # print(Pow(Pow(Num(2), Num(3)), Num(4)))
    # # (2 ** 3) ** 4
