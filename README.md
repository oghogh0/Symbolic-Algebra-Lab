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
I added support for checking if two expressions are equal. In doing this, I added this method to the following subclasses<br/>

1. Var:<br/>

       def __eq__(self, other):
            if (
                isinstance(self, type(other)) and self.name == other.name
            ):  # check same class and contents
                return True
            return False
<br/>
3. Num: <br/>

        def __eq__(self, other):
            if isinstance(self, type(other)) and self.n == other.n:
                return True
            return False
<br/>
3. BinOp: <br/>
  
        def __eq__(self, other):
            if (
                isinstance(self, type(other))
                and self.left == other.left
                and self.right == other.right
            ):
                return True
            return False
<br/>
<p align="left">
SIMPLIFICATION:<br/>
I have added a method called simplify to various classes, which returns a simplified form of the given expression, according to the following rules:<br/>
- Any binary operation on two numbers simplifies to a single number containing the result.<br/>
- Adding 0 to (or subtracting 0 from) any expression E simplifies to E.<br/>
- Multiplying or dividing any expression E by 1 simplifies to E.<br/>
- Multiplying any expression E by 0 simplifies to 0.<br/>
- Dividing 0 by any expression E simplifies to 0.<br/>
- A single number or variable always simplifies to itself.<br/>

I added this method to the following subclasses:<br/>
1. Symbol:<br/>

        def simplify(self):
            return self  # var and num the same
<br/>
2. Add: <br/>

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
<br/>
3. Subtract:<br/>
    
        def simplify(self):
            simplified_left = self.left.simplify()
            simplified_right = self.right.simplify()
    
            if isinstance(simplified_left, Num) and isinstance(simplified_right, Num):
                return Num(simplified_left.n - simplified_right.n)
    
            if simplified_right == Num(0):  # only simplifies on right not 0-x
                return simplified_left
    
            return Sub(simplified_left, simplified_right)

<br/>
4. Multiply:<br/>

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
<br/>
5. Divide:<br/>
    
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
<br/>
6. Exponentiate:<br/>

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

<br/>
<p align="left">
DERIVATION:<br/>
Undergoes derivation of different expressions. I added this method to the following subclasses:<br/>
1. Var:<br/>
    
        def deriv(self, item):
            if self.name == item:  # base case 1
                return Num(1)
            return Num(0)

<br/>
2. Num: <br/>

        def deriv(self, item):
            return Num(0)  # base case 2
<br/>

3. Add:<br/>
    
        def deriv(self, item):
            return Add(self.left.deriv(item), self.right.deriv(item))
<br/>

4. Subtraction: <br/>
   
        def deriv(self, item):
            return Sub(self.left.deriv(item), self.right.deriv(item))
<br/>

5. Multiplication:<br/>
   
        def deriv(self, item):
            return Add(
                Mul(self.left, self.right.deriv(item)),
                Mul(self.right, self.left.deriv(item)),
            )
<br/>

5. Division:<br/>
   
        def deriv(self, item):
            return (
                Sub(
                    Mul(self.right, self.left.deriv(item)),
                    Mul(self.left, self.right.deriv(item)),
                )
            ) / Mul(
                self.right, self.right
            )  # square

<br/>

6. Exponentiation:<br/>

        def deriv(self, item):
            if isinstance(self.right, Num):
                return Mul(
                    Mul(self.right, Pow(self.left, self.right - 1)), self.left.deriv(item)
                )
            raise TypeError
<br/>
<p align="left">
EXPRESSIONS:<br/>   
Lastly, I have added support to parse strings into symbolic expressions (to provide yet another means of input). It takes in a single string containing either a single variable name, a single number, or a fully parenthesised expression of the form (E1 op E2), representing a binary operation (where E1 and E2 are themselves strings representing expressions, and op is one of +, -, *, or /). An assumption made is that the string is always well-formed and fully parenthesised (don't need to handle erroneous input), but it works for arbitrarily deep nesting of expressions. The implementation of this function expression does not use Python's built-in eval, exec, type, or isinstance functions.<br/> 
    
This process is broken down into two pieces: tokenising (to break the input string into meaningful units) and parsing (to build our internal representation from those units). <br/> 

For example, calling expression('(x * (2 + 3))') parses to Mul(Var('x'), Add(Num(2), Num(3))).<br/> 

1. Tokenising: takes in a string as described above and outputs a list of meaningful tokens (parentheses, variable names, numbers, or operands). An assumption made is that variables are always single-character alphabetic characters and that all numbers are positive or negative integers or floats. Also assume that there are spaces separating operands and operators. This code also handles numbers with more than one digit and negative numbers. A number like -200.5, for example, should be represented by a single token '-200.5'.<br/> 

For example, calling tokenize("(x * (2 + 3))") returns:<br/> 
<br/>
['(', 'x', '*', '(', '2', '+', '3', ')', ')']

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
<br/> 
2. Parsing: takes in the output of tokenize, converting it into an appropriate instance of Symbol (or some subclass thereof).<br/> 

For example, calling parse(tokenize("(x * (2 + 3))")) returns:<br/> 
<br/>
Mul(Var('x'), Add(Num(2), Num(3)))
<br/> 
For this function, I created a helper function 'find_class', which determines a class given its corresponding operand.<br/> 

    if operand == "+":
        return Add
    elif operand == "-":
        return Sub
    elif operand == "*":
        return Mul
    elif operand == "/":
        return Div
    else:  # "**"
        return Pow

Another function called 'parse_expression' is defined in the 'parse' function. It is a recursive function that takes in an integer indexing into the tokens list and returns a pair of values. The expression found starting at the location given by index (an instance of one of the Symbol subclasses), and the index beyond where this expression ends (e.g., if the expression ends at the token with index 6 in the tokens list, then the returned value should be 7). In the definition of this procedure, it is important to call it with the value index corresponding to the start of an expression. So, there are 3 cases that need to be handled. Let token be the token at location index; the cases are:<br/> 

1. Number: if token represents an integer or a float, then make a corresponding Num instance and return that, paired with index + 1 (since a number is represented by a single token).<br/> 
2. Variable: if token represents a variable name (a single alphabetic character), then make a corresponding Var instance and return that, paired with index + 1 (since a variable is represented by a single token).<br/> 
3. Operation: otherwise, the sequence of tokens starting at index must be of the form: (E1 op E2). Therefore, token must be (. In this case, recursively parse the two subexpressions, combine them into an appropriate instance of a subclass of BinOp (determined by op), and return that instance, along with the index of the token beyond the final right parenthesis.<br/> 


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
    
        parsed_expression, next_index = parse_expression(0)
        return parsed_expression
    
<br/> 
The code for 'expression' looks like this:

     return parse(tokenize(statement))







