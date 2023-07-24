<h1>Symbolic Algebra Lab</h1>
<h2>Description</h2>
In this lab, I develop a Python framework for symbolic algebra. In such a system, algebraic expressions including variables and numbers are not immediately evaluated but rather are stored in symbolic form. These kinds of systems abound in the "real world," and they can be incredibly useful. Examples of similar systems include Wolfram Alpha and Sympy. <br />

I'll start by implementing support for basic arithmetic (+, -, *, and /) on variables and numbers, and then add support for simplification and differentiation of these symbolic expressions. Ultimately, this system will be able to support numerous interactions as shown below. <br />

<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through</h2>

<p align="left">
Create the BASE CLASS, 'Symbol':<br/>
All other classes created in this lab inherits from this class, and any behaviour that is common between all expressions (that is, all behaviour that is not unique to a particular kind of symbolic expression) is implemented here. Such behaviours include:<br/>
- addition & subtraction<br/>
- multiplication & division<br/>
- indices<br/>
- evaluation: for any symbolic expression sym, sym.eval(mapping) finds a numerical value for the given expression. The mapping is a dictionary mapping variable names to values.<br/>

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

