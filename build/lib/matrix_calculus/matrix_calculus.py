%%writefile matrix_calculus.py
########################################################################
# Matrix Calculus
# This library is based on the online tool http://www.matrixcalculus.org/
# Author: Ray 
# Email: songlinhou1993@gmail.com
########################################################################

from IPython.core.display import TextDisplayObject
import string
from copy import deepcopy
import requests

DEFAULT_N_ROWS = 5
DEFAULT_N_COLS = 5

__version__ = 0.1
__author__ = 'Ray'
__email__ = 'songlinhou1993@gmail.com'

class Terms(TextDisplayObject):
    pass


class Operators(Terms):
    @staticmethod
    def __check_expression(name, expr):
        assert type(expr) is Expression, "{} must be {}, got type {} instead.".format(name, Expression,type(expr))

    @staticmethod
    def binary_op(op, expr1, expr2):
        Operators.__check_expression('expr1', expr1)
        Operators.__check_expression('expr2', expr2)

        c1 = expr1.contents
        c2 = expr2.contents
        expr_list  = c1 + [op] + c2
        return Expression(expr_list)

    @staticmethod
    def add(expr1, expr2):
        return Operators.binary_op("+",expr1, expr2)

    @staticmethod
    def minus(expr1, expr2):
        return Operators.binary_op("-",expr1, expr2)

    @staticmethod
    def multiply(expr1, expr2):
        return Operators.binary_op("*",expr1, expr2)

    @staticmethod
    def divide(expr1, expr2):
        return Operators.binary_op("/",expr1, expr2)

    @staticmethod
    def power(expr1, expr2):
        return Operators.binary_op("^",expr1, expr2)

    @staticmethod
    def element_wise_multiply(expr1, expr2):
        return Operators.binary_op(".*",expr1, expr2)

    @staticmethod
    def element_wise_division(expr1, expr2):
        return Operators.binary_op("./",expr1, expr2)

    @staticmethod
    def element_wise_power(expr1, expr2):
        return Operators.binary_op(".^",expr1, expr2)



class Matrix(Terms):
    def __init__(self, symbol, is_symmetric=False, n_rows=None, n_cols=None, naming_check=True):
        assert type(symbol) == str, "symbol must be str, got type {} instead.".format(type(symbol))
        assert len(symbol) > 0, "symbol must be a valid str"
        self.chars = [c for c in symbol]
        if naming_check:
            assert self.chars[0] in string.ascii_uppercase, "first letter in matrix must be uppercase letter."
        allowed_chars = [c for c in string.ascii_uppercase] + [c for c in string.ascii_lowercase] + [c for c in string.digits]
        for c in self.chars:
            if c not in allowed_chars:
                assert False, "{} is not allowed to define a symbol".format(c)
        self.symbol = symbol
        self.is_symmetric = is_symmetric
        self.n_rows = DEFAULT_N_ROWS if n_rows is None else n_rows
        self.n_cols = DEFAULT_N_COLS if n_cols is None else n_cols
        self.is_transposed = False
        self.T = self.transpose()
        self.var_type = 'matrix'
        if is_symmetric:
            self.var_type = 'symmetric matrix'

    def _repr_latex_(self):
        s = self.symbol.strip('$')
        return "$$%s$$" % s

    def to_expression(self):
        return Expression([self])


    # def __str__(self):
    #     return "Matrix({}, is_symmetric={})".format(self.symbol, self.is_symmetric)

    def __str__(self):
        return self.symbol

    def transpose(self):
        other = deepcopy(self)
        if other.is_transposed:
            other.symbol = other.symbol.replace("'","")
            other.is_transposed = False
        else:
            other.symbol = other.symbol + "'"
            other.is_transposed = True
        return other

    def __add__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.add(this, other)
        other = Expression([other])
        return Operators.add(this, other)

    def __radd__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.add(other, this)
        other = Expression([other])
        return Operators.add(other, this)

    def __sub__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.minus(this, other)
        other = Expression([other])
        return Operators.minus(this, other)

    def __rsub__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.minus(other, this)
        other = Expression([other])
        return Operators.minus(other, this)

    def __mul__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.multiply(this, other)
        other = Expression([other])
        return Operators.multiply(this, other)

    def __rmul__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.multiply(other, this)
        other = Expression([other])
        return Operators.multiply(other, this)


    def __truediv__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.divide(this, other)
        other = Expression([other])
        return Operators.divide(this, other)

    def __rtruediv__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.divide(other, this)
        other = Expression([other])
        return Operators.divide(other, this)

    def __div__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.divide(this, other)
        other = Expression([other])
        return Operators.divide(this, other)

    def __rdiv__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.divide(other, this)
        other = Expression([other])
        return Operators.divide(other, this)

    
    def __pow__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.power(this, other)
        other = Expression([other])
        return Operators.power(this, other)

    def __rpow__(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.power(other, this)
        other = Expression([other])
        return Operators.power(other, this)

    def elem_mult(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.element_wise_multiply(this, other)
        other = Expression([other])
        return Operators.element_wise_multiply(this, other)

    def elem_div(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.element_wise_division(this, other)
        other = Expression([other])
        return Operators.element_wise_division(this, other)

    def elem_pow(self, other):
        this = self.to_expression()
        if type(other) is Expression:
            return Operators.element_wise_power(this, other)
        other = Expression([other])
        return Operators.element_wise_power(this, other)

class Vector(Matrix):
    def __init__(self, symbol, n_rows=None):
        super().__init__(symbol, False, n_rows, None, False)
        assert self.chars[0] in string.ascii_lowercase, "first letter in vector must be lowercase letter."
        self.var_type = 'vector'
       
        
class Scalar(Matrix):
    def __init__(self, symbol):
        super().__init__(symbol, False, None, None, False)
        assert self.chars[0] in string.ascii_lowercase, "first letter in scalar must be lowercase letter."
        self.var_type = 'scalar'
        


class Expression(Terms):
    def __init__(self, contents):
        self.contents = contents
        syms = []
        for sym in contents:
            if type(sym) in [Matrix, Vector]:
                syms.append(sym.symbol)
            else:
                syms.append(str(sym))
        self.syms = syms
        self.repr = "".join(syms)
        self.is_transposed = False
        if self.syms[-1] == "'":
            self.is_transposed = True
        self.T = self.to_transpose()


    def to_transpose(self):
        if self.is_transposed:
            contents = deepcopy(self.contents)
            contents = contents[:-1]
            if contents[0] == "(" and contents[-1] == ")":
                contents = contents[1:-1]
        else:
            contents = deepcopy(self.contents)
            if contents[0] == "(" and contents[-1] == ")":
                contents.append("'")
            else:
                contents = ['('] + contents + [')', "'"]
            return Expression(contents)


    def __repr__(self):
        return self.repr

    def __str__(self):
        return self.repr

    def __add__(self, other):
        expr_list = self.contents
        expr_list += ["+", other]
        return Expression(expr_list)

    def __radd__(self, other):
        if type(other) is not Expression:
            expr_list = [other]
        else:
            expr_list = other.contents
        expr_list += ["+"] + self.contents
        return Expression(expr_list)

    def __sub__(self, other):
        expr_list = self.contents
        expr_list += ["-", other]
        return Expression(expr_list)

    def __rsub__(self, other):
        if type(other) is not Expression:
            expr_list = [other]
        else:
            expr_list = other.contents
        expr_list += ["-"] + self.contents
        return Expression(expr_list)

    def __mul__(self, other):
        expr_list = self.contents
        expr_list += ["*", other]
        return Expression(expr_list)

    def __rmul__(self, other):
        if type(other) is not Expression:
            expr_list = [other]
        else:
            expr_list = other.contents
        expr_list += ["*"] + self.contents
        return Expression(expr_list)

    def __div__(self, other):
        expr_list = self.contents
        expr_list += ["/", other]
        return Expression(expr_list)

    def __rdiv__(self, other):
        if type(other) is not Expression:
            expr_list = [other]
        else:
            expr_list = other.contents
        expr_list += ["/"] + self.contents
        return Expression(expr_list)

    def __truediv__(self, other):
        expr_list = self.contents
        expr_list += ["/", other]
        return Expression(expr_list)

    def __rtruediv__(self, other):
        if type(other) is not Expression:
            expr_list = [other]
        else:
            expr_list = other.contents
        expr_list += ["/"] + self.contents
        return Expression(expr_list)

    def __pow__(self, other):
        expr_list = self.contents
        expr_list += ["^", "(",other,")"]
        return Expression(expr_list)

    def __rpow__(self, other):
        if type(other) is not Expression:
            expr_list = [other]
        else:
            expr_list = other.contents
        expr_list += ["^", "("] + self.contents + [")"]
        return Expression(expr_list)

    def elem_mult(self, other):
        expr_list = self.contents
        expr_list += [".*", other]
        return Expression(expr_list)

    def elem_div(self, other):
        expr_list = self.contents
        expr_list += ["./", other]
        return Expression(expr_list)

    def elem_pow(self, other):
        expr_list = self.contents
        expr_list += [".^", other]
        return Expression(expr_list)

def term(expression):
    if type(expression) is Expression:
        contents = expression.contents
        contents = ["("] + contents + [")"]
        return Expression(contents)
    return Expression([expression])

def t(expression):
    return term(expression)

def apply_operator(op, expression):
    if type(expression) is Expression:
        contents = expression.contents
    else:
        contents = [expression]
    contents = [op + "("] + contents + [")"]
    return Expression(contents)

def func(op, expression):
    return apply_operator(op, expression)


### functions

def sin(expression):
    return apply_operator('sin', expression)

def cos(expression):
    return apply_operator('cos', expression)

def tan(expression):
    return apply_operator('tan', expression) 

def arcsin(expression):
    return apply_operator('arcsin', expression) 

def arccos(expression):
    return apply_operator('arccos', expression) 

def arctan(expression):
    return apply_operator('arctan', expression) 

def log(expression):
    return apply_operator('log', expression) 

def exp(expression):
    return apply_operator('exp', expression) 

def tanh(expression):
    return apply_operator('tanh', expression) 

def abs(expression):
    return apply_operator('abs', expression) 

def sign(expression):
    return apply_operator('sign', expression) 

def relu(expression):
    return apply_operator('relu', expression) 

def sum(expression):
    return apply_operator('sum', expression) 

def norm1(expression):
    return apply_operator('norm1', expression) 

def norm2(expression):
    return apply_operator('norm2', expression) 

def tr(expression):
    return apply_operator('tr', expression) 

def det(expression):
    return apply_operator('det', expression) 

def inv(expression):
    return apply_operator('inv', expression) 

def logdet(expression):
    return apply_operator('logdet', expression) 

def vector(expression):
    return apply_operator('vector', expression) 

def matrix(expression):
    return apply_operator('matrix', expression) 


#######################

def check_var_type(var):
    try:
        var_data = {"name": var.symbol}
        var_data['type']  = var.var_type
    except:
        assert False, "find unacceptable variable {} with types other than scalar, vector and matrix".format(var)
    return var_data

def check_symbol_unique(var_list):
    syms = [var.symbol for var in var_list]
    if len(set(syms)) == len(syms):
        return True
    return False


def post_info(expr_str, wrt_var, var_list):
    assert check_symbol_unique(var_list), "find variables with identical name."
    json_data = {}
    json_data['expression'] = expr_str
    json_data['wrt'] = check_var_type(wrt_var)
    assert wrt_var in var_list, "wrt_var is not included in var_list"
    var_json_list = []
    var_json_list = [check_var_type(var) for var in var_list]
    json_data['varList'] = var_json_list
    json_data['n'] = len(var_json_list)
    return json_data

def strip_before(content, query):
    return content[content.index(query) + len(query):]

def strip_end(content, query):
    return content[:content.index(query)]

def keep_between(content, query_start, query_end):
    content = strip_before(content, query_start)
    content = strip_end(content, query_end)
    return content.strip()

def diff(expr, wrt_var, var_list, return_tex=False):
    assert type(expr) is Expression, "expr must be of type {} but got {}".format(Expression, type(expr)) 
    json_data = post_info(str(expr), wrt_var, var_list)
    url = "http://www.matrixcalculus.org/_show"
    data = json_data
    r = requests.post(url=url, json=data)
    if r.status_code // 100 != 2:
        assert False, "network issue"
    service_resp = r.json()
    name = service_resp['wrt']
    expressionLatex = service_resp['expressionLatex']
    tex = '\\frac{\\partial}{\\partial ' + name +'} \\left( ' + expressionLatex + ' \\right) = '
    derivative = service_resp['derivative']

    if (len(expressionLatex) + len(derivative) > 120):
        tex = tex + '\\\\\\quad\\quad '

    tex = tex + derivative
    error = service_resp['errorString'].strip()
    if len(error)  > 0:
        # find error
        raise Exception(error)
    if return_tex:
        return tex
    try:
        if not return_tex:
            from IPython.display import Math, HTML
            display(HTML("<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.3/"
                          "latest.js?config=default'></script>"))
            out = Math(tex)
            return out
    except:
        print("only accessible in interative environments such as Colab and Jupyter Notebook. Switch back to show tex.")
    return tex

if __name__ == '__main__':
    x = Vector("x")
    A = Matrix("A")
    c = Scalar('c')
    y = Vector("y")
    formula = x.T * A * x + c * sin(y).T * x
    out = diff(formula, x, [x, A, c, y], True)
    print("answer is", out)