<h1>Symbolic Algebra Lab</h1>
<h2>Description</h2>
In this lab, I develop a Python framework for symbolic algebra. In such a system, algebraic expressions including variables and numbers are not immediately evaluated but rather are stored in symbolic form. These kinds of systems abound in the "real world," and they can be incredibly useful. Examples of similar systems include Wolfram Alpha and Sympy. <br /> 

I'll start by implementing support for basic arithmetic (+, -, *, and /) on variables and numbers, and then add support for simplification and differentiation of these symbolic expressions. Ultimately, this system will be able to support numerous interactions as shown below. Each operation's precedence is defined using the standard "PEMDAS" ordering. A higher precedence value indicates a hgiher precedence. <br />

<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through</h2>

<p align="left">
Create the BASE CLASS, 'Symbol':<br/>
This class has a precedence of 0.All other classes created in this lab inherits from this class, and any behaviour that is common between all expressions (that is, all behaviour that is not unique to a particular kind of symbolic expression) is implemented here. Such behaviours include:<br/>
- addition & subtraction<br/>
- multiplication & division<br/>
- exponentiation<br/>
    
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




<br/>
<p align="left">
VAR and NUM subclasses:<br/>
I assigned Var and Num to have a precedence of 3. Instances of Var represent variables (such as x or y) whilst instances of Num represent numbers within symbolic expressions. The following class is given <br/>
1. Var: <br/>
    
    def __init__(self, n):
        self.name = n
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"Var('{self.name}')"
<br/>
2. Num:<br/>

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"
<br/>

<p align="left">
BINARY OPERATIONS:<br/>
BinOp has precedence 0. This class, BinOp represents a binary operation. It is a type of symbolic expression and is therefore a subclass of Symbol. By virtue of being binary operations, any subclass of BinOp has two instance variables: left - a Symbol instance representing the left-hand operand, and right - a Symbol instance representing the right-hand operand. Importantly, instances or subclasses of BinOp should only have these two instance attributes. We consider parenthesisation rules with each operation's precedence defined using the standard "PEMDAS" ordering.<br/>

    precedence = 0
    right_parens = False
    left_parens = False

    def __init__(self, left, right):
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

<br/>
<p align="left">
Create BinOp SUBCLASSES:<br/>
Addition and Subtraction have precedence of 1. Multiplication, Division and Exponentiation have precedence of 2.  <br/>
1. Add: E1 + E2 results in an instance Add(E1, E2) <br/>
   
    operand = "+"
    precedence = 1
    right_parens = False
    left_parens = False
<br/>
2. Subtract: E1 - E2 results in an instance Sub(E1, E2)<br/>

    operand = "-"
    precedence = 1
    right_parens = True
    left_parens = False
<br/>
3. Multiplication: E1 * E2 results in an instance Mul(E1, E2)<br/>

    operand = "*"
    precedence = 2
    right_parens = False
    left_parens = False
<br/>
4. Division: E1 / E2 results in an instance Div(E1, E2)<br/>

    operand = "/"
    precedence = 2
    right_parens = True
    left_parens = False
<br/>
5. Exponentiation: E1 ** E2 results in an instance Pow(E1, E2)<br/>

    operand = "**"
    precedence = 2
    right_parens = False
    left_parens = True 
<br/>
<p align="left">
EVALUATION:<br/>
Next, I have added support for evaluating expressions for particular values of variables. In doing this, I added methods to various classes or subclasses such that, for any symbolic expression sym, sym.eval(mapping) will find a numerical value (meaning a float or an int, not an instance of Num) for the given expression. This mapping is a dictionary mapping variable names to values.<br/>

1. Symbol:<br/>

        def eval(self, mapping):
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

<br/>
2. Var:<br/>

    def eval(self, mapping):  # base case
        if self.name not in mapping:
            raise NameError
        return mapping[self.name]
<br/>
3. Num:<br/>

    def eval(self, mapping):  # base case iof eval
        return self.n
   
<br/>

<p align="left">
EQUALITY:<br/>
I added support for checking if two expressions are equal. In doing this, I added methods to the following subclasses<br/>

1. Var:<br/>
    def __eq__(self, other):
            if (
                isinstance(self, type(other)) and self.name == other.name
            ):  # check same class and contents
                return True
            return False
<br/>
2. Num: <br/>

<br/>
3. BinOp: <br/>
<br/>
- simplify: returns a simplified form of the expression, according to the following rules:<br/>
<p align="center">
  Any binary operation on two numbers simplifies to a single number containing the result.<br/>
  Adding 0 to (or subtracting 0 from) any expression E simplifies to E.<br/>
  Multiplying or dividing any expression E by 1 simplifies to E.<br/>
  Multiplying any expression E by 0 simplifies to 0.<br/>
  Dividing 0 by any expression E should simplifies to 0.<br/>
  A single number or variable always simplifies to itself.<br/>
This function is the same for var and num so can be added as an attribute to the 'Symbol' class. 


class Symbol:
    def simplify(self):
        return self  # var and num the same


class Var(Symbol):
    

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


    def __eq__(self, other):
        if isinstance(self, type(other)) and self.n == other.n:
            return True
        return False

    def deriv(self, item):
        return Num(0)  # base case 2


# subclass of Symbol
class BinOp(Symbol):
    
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


