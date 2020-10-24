import ply.yacc as yacc

from lexer import tokens


class Type: pass

class SimpleType(Type):
    def __init__(self, type_name):
        self.type = type_name

def p_SimpleType(p):
    '''TYPE : int
          | float
          | cint
          | sfloat
          | void'''
    p[0] = SimpleType(p[1])

class RefType(Type):
    def __init__(self, type):
        self


class Vdecl:
    def __init__(self, type, varid):
        self.type = ''





class Expr: pass

class BinOp(Expr):
    def __init__(self,left,op,right):
        self.left = left
        self.right = right
        self.op = op

    def yaml(self): #每个定义的class都要改
        self.left.yaml()
        print(self.op)
        self.right.yaml()

class Number(Expr):
    def __init__(self,value):
        self.value = value
    
    def yaml(self):
        print(self.value)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = BinOp(p[1],p[2],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])

data = '''
1 + 2 + 3
'''

yacc.yacc(start = 'expression')
ast = yacc.parse(data, debug = False)
ast.yaml()
