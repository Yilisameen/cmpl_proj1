import ply.yacc as yacc

from lexer import tokens

class Exps:
    def __init__(self, exp):
        self.exps = []
        self.exps.append(exp)

    def addExp(self, exp):
        self.exps.append(exp)

    def yaml(self, prefix = ''):
        print(prefix + 'name: exps')
        print(prefix + 'exps:')
        prefix = prefix + ' '
        for i in range(len(self.exps)-1, -1, -1):
            print(prefix + '-')
            self.exps[i].yaml(prefix + ' ')

def p_exps(p):
    '''EXPS : EXP
            | EXP COMMA EXPS'''
    if len(p) == 2:
        p[0] = Exps(p[1])
    elif len(p) == 4:
        p[3].addExp(p[1]) 
        p[0] = p[3]

class Exp:
    def __init__(self, exp):
        self.style = 'exp'
        self.exp = exp

    def yaml(self, prefix = ''):
        self.exp.yaml(prefix)

def p_exp(p):
    '''EXP : EXPPAREN
            | BINOP
            | UOP
            | LIT
            | VARID
            | EXPGLOBID'''
    p[0] = Exp(p[1])

class ExpParen:
    def __init__(self, exp):
        self.style = 'expParen'
        self.exp = exp
    
    def yaml(self, prefix = ''):
        self.exp.yaml(prefix)

def p_expParen(p):
    '''EXPPAREN : LPAREN EXP RPAREN'''
    p[0] = ExpParen(p[2])

class ExpGlobID:
    def __init__(self, globid, params):
        self.style = 'expGlobID'
        self.globid = globid
        self.params = params
    
    def yaml(self, prefix = ''):
        print(prefix + 'name: funccall')
        print(prefix + 'globid: ' + self.globid)
        print(prefix + 'params: ')
        self.params.yaml(prefix + ' ')

def p_expGlobid(p):
    '''EXPGLOBID : GLOBID EXPWRAPPER'''
    p[0] = ExpGlobID(p[1], p[2])

def p_expWrapper(p):
    '''EXPWRAPPER : LPAREN RPAREN
                | LPAREN EXPS RPAREN'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

class Assign:
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp

    def yaml(self, prefix = ''):
        print(prefix + 'name: assign')
        self.var.yaml(prefix)
        print(prefix + 'exp:')
        self.exp.yaml(prefix + ' ')

def p_assign(p):
    '''ASSIGN : VARID EQUAL EXP'''
    p[0] = Assign(p[1], p[3])

class TypeCast:
    def __init__(self, typename, exp):
        self.typename = typename
        self.exp = exp

    def yaml(self, prefix = ''):
        print(prefix + 'name: caststmt')
        self.typename.yaml(prefix)
        print(prefix + 'exp:')
        self.exp.yaml(prefix + ' ')

def p_typeCast(p):
    '''TYPECAST : LBRACKET TYPE RBRACKET EXP'''
    p[0] = TypeCast(p[2], p[4])

class Binop:
    def __init__(self, value):
        self.value = value
    
    def yaml(self, prefix = ''):
        self.value.yaml(prefix)

def p_binop(p):
    '''BINOP : ARITHOPS
            | LOGICOPS
            | ASSIGN
            | TYPECAST'''
    p[0] = Binop(p[1])


class ArithOps:
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def yaml(self, prefix = ''):
        print(prefix + 'op: ' + self.op)
        print(prefix + 'lhs: ')
        self.lhs.yaml(prefix + ' ')
        print(prefix + 'rhs: ')
        self.lsh.yaml(prefix + ' ')

def p_arithOps(p):
    '''ARITHOPS : EXP TIMES EXP
                | EXP DIVIDE EXP
                | EXP PLUS EXP
                | EXP MINUS EXP'''
    if p[2] == '*':
        p[0] = LogicOps('mul', p[1], p[3])
    elif p[2] == '/':
        p[0] = LogicOps('div', p[1], p[3])
    elif p[2] == '+':
        p[0] = LogicOps('add', p[1], p[3])
    elif p[2] == '-':
        p[0] = LogicOps('sub', p[1], p[3])


class LogicOps:
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def yaml(self, prefix = ''):
        print(prefix + 'op: ' + self.op)
        print(prefix + 'lhs: ')
        self.lhs.yaml(prefix + ' ')
        print(prefix + 'rhs: ')
        self.rhs.yaml(prefix + ' ')

def p_logicOps(p):
    '''LOGICOPS : EXP EQUALITY EXP
                | EXP LESS EXP
                | EXP GREATER EXP
                | EXP AND EXP
                | EXP OR EXP'''
    if p[2] == '==':
        p[0] = LogicOps('eq', p[1], p[3])
    elif p[2] == '<':
        p[0] = LogicOps('lt', p[1], p[3])
    elif p[2] == '>':
        p[0] = LogicOps('gt', p[1], p[3])
    elif p[2] == '&&':
        p[0] = LogicOps('and', p[1], p[3])
    elif p[2] == '||':
        p[0] = LogicOps('or', p[1], p[3])


class Uop:
    def __init__(self, exp, op):
        self.exp = exp
        self.op = op

    def yaml(self, prefix = ''):
        print(prefix + 'name: uop')
        print(prefix + 'op: ' + self.op)
        print(prefix + 'exp: ')
        prefix = prefix + ' '
        #self.exp.yaml(prefix)
        print(prefix + self.exp)

def p_uop(p):
    '''UOP : NOT EXP
            | MINUS EXP'''
    if p[1] == '-':
        p[0] = Uop(p[2], 'minus')
    else:
        p[0] = Uop(p[2], 'not')
    # error handle missing
        

class Lit:
    def __init__(self, value):
        self.value = value

    def yaml(self, prefix = ''):
        print(prefix + 'name: lit')
        print(prefix + 'value: ' + self.value)

def p_lit(p):
    '''LIT : TRUE
            | FALSE
            | NUMBER'''
    p[0] = Lit(p[1])

class Tdecls:
    def __init__(self, typename):
        self.types = []
        self.types.append(typename)

    def addType(self, typename):
        self.types.append(typename)

    def yaml(self, prefix = ''):
        # print(prefix + 'vdecls')
        # prefix = prefix + ' '
        print(prefix + 'name: tdecls')
        print(prefix + 'types:')
        prefix = prefix + ' '
        for i in range(len(self.types)-1, -1, -1):
            print(prefix + '- ' + self.types[i].value)

def p_tdecls(p):
    '''TDECLS : TYPE
                | TYPE COMMA TDECLS'''
    if len(p) == 2:
        p[0] = Tdecls(p[1])
    else :
        p[3].addType(p[1])
        p[0] = p[3]

class Vdecls:
    def __init__(self, vdecl):
        self.vars = []
        self.vars.append(vdecl)
    
    def addVar(self, vdecl):
        self.vars.append(vdecl)

    def yaml(self, prefix = ''):
        # print(prefix + 'vdecls')
        # prefix = prefix + ' '
        print(prefix + 'name: vdecls')
        print(prefix + 'vars:')
        prefix = prefix + ' '
        for i in range(len(self.vars)-1, -1, -1):
            current_prefix = prefix
            print(prefix + '-')
            current_prefix = current_prefix + ' '
            self.vars[i].yaml(current_prefix)


def p_vdecls(p):
    '''VDECLS : VDECL COMMA VDECLS
            | VDECL'''
    
    if len(p) == 4:
        p[3].addVar(p[1])
        p[0] = p[3]
    else:
        vdecls = Vdecls(p[1])
        p[0] = vdecls

class Vdecl:
    def __init__(self, typename, var):
        self.typename = typename
        self.var = var

    def yaml(self, prefix = ''):
        # print(prefix + 'vdecl:')
        # prefix = prefix + ' '
        print(prefix + 'node: vdecl')
        self.typename.yaml(prefix)
        self.var.yaml(prefix)

def p_vdecl(p):
    '''VDECL : TYPE VARID'''
    p[0] = Vdecl(p[1], p[2])

class Varid:
    def __init__(self, value):
        self.value = value
    
    def yaml(self, prefix = ''):
        print(prefix + 'var: ' + self.value)

def p_varid(p):
    '''VARID : DOLLAR ID'''
    value = p[1] + p[2]
    p[0] = Varid(value)


class GlobalID:
    def __init__(self, value):
        self.value = value

    def yaml(self, prefix = ''):
        print(prefix + 'globid: ' + self.value)

def p_globid(p):
    '''GLOBID : ID'''
    p[0] = GlobalID(p[1])


class Type:
    def __init__(self, value):
        self.value = value

    def yaml(self, prefix = ''):
        print(prefix + 'type: ' + self.value)

def p_simpleType(p):
    '''TYPE : INT
          | FLOAT
          | CINT
          | VOID'''
    p[0] = Type(p[1])

def p_refType(p):
    '''TYPE : REF TYPE'''
    value = 'ref ' + p[2].value
    p[0] = Type(value)

def p_refTypeNoAlias(p):
    '''TYPE : NOALIAS REF TYPE'''
    value = 'noalias ref ' + p[3].value
    p[0] = Type(value)

precedence = (
  ('right', 'EQUAL'),
  ('left', 'OR'),
  ('left', 'AND'),
  ('left', 'EQUALITY'),
  ('left', 'LESS', 'GREATER'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES','DIVIDE'),
  #('left','UOP')
)

data = '''
$x = [int] ($a + $b - $c / $a * $b)
'''

yacc.yacc(start = 'EXPS')
ast = yacc.parse(data, debug = False)
ast.yaml()
