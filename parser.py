import ply.yacc as yacc

from lexer import tokens

class Exps:
    def __init__(self, exp):
        self.exps = []
        self.exps.append(exp)

    def addExp(self, exp):
        self.exps.append(exp)

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: exps\n'
        res = prefix + 'exps:\n'
        prefix = prefix + ' '
        for i in range(len(self.exps)-1, -1, -1):
            res = res + prefix + '-\n'
            res = res + self.exps[i].yaml_format(prefix + ' ')
        return res

class Exp:
    def __init__(self, exp):
        self.type = 'exp'
        #self.style = 'exp'
        self.exp = exp

    def yaml_format(self, prefix = ''):
        res = ''
        if self.exp.type == 'varid':
            res = prefix + 'name: varval\n'
        res= res + self.exp.yaml_format(prefix)
        return res

class Binop:
    def __init__(self, value):
        self.type = 'binop'
        self.value = value
    
    def yaml_format(self, prefix = ''):
        if self.value.type == 'typeCast':
            res = prefix + 'name: caststmt\n'
        elif self.value.type == 'assign':
            res = prefix + 'name: assign\n'
        elif self.value.type == 'expGlobID':
            res = prefix + 'name: funccall\n'
        else:
            res = prefix + 'name: binop\n'
        res = res + self.value.yaml_format(prefix)
        return res

class ExpParen:
    def __init__(self, exp):
        self.type = 'expParen'
        #self.style = 'expParen'
        self.exp = exp
    
    def yaml_format(self, prefix = ''):
        return self.exp.yaml_format(prefix)

class ExpGlobID:
    def __init__(self, globid, params):
        self.type = 'expGlobID'
        #self.style = 'expGlobID'
        self.globid = globid
        self.params = params
    
    def yaml_format(self, prefix = ''):
        #res = prefix + 'name: funccall\n'
        res = prefix + 'globid: ' + self.globid + '\n'
        if self.params is not None:
            res = res + prefix + 'params: \n'
            res = res + self.params.yaml_format(prefix + ' ')
        return res


class Assign:
    def __init__(self, var, exp):
        self.type = 'assign'
        self.var = var
        self.exp = exp

    def yaml_format(self, prefix = ''):
        #print(prefix + 'name: assign')
        res = self.var.yaml_format(prefix)
        res = res + prefix + 'exp:\n'
        res = res + self.exp.yaml_format(prefix + ' ')
        return res

class TypeCast:
    def __init__(self, typename, exp):
        self.type = 'typeCast'
        self.typename = typename
        self.exp = exp

    def yaml_format(self, prefix = ''):
        res = self.typename.yaml_format(prefix)
        res = res + prefix + 'exp:\n'
        res = res + self.exp.yaml_format(prefix + ' ')
        return res

class ArithOps:
    def __init__(self, op, lhs, rhs):
        self.type = 'arithOps'
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def yaml_format(self, prefix = ''):
        res = prefix + 'op: ' + self.op + '\n'
        res = res + prefix + 'lhs: \n'
        res = res + self.lhs.yaml_format(prefix + ' ')
        res = res + prefix + 'rhs: '
        res = res + self.lsh.yaml_format(prefix + ' ')
        return res

class LogicOps:
    def __init__(self, op, lhs, rhs):
        self.type = 'logicOps'
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def yaml_format(self, prefix = ''):
        res = prefix + 'op: ' + self.op + '\n'
        res = res + prefix + 'lhs: \n'
        res = res + self.lhs.yaml_format(prefix + ' ') + '\n'
        res = res + prefix + 'rhs: \n'
        res = res + self.rhs.yaml_format(prefix + ' ') + '\n'
        return res

class Uop:
    def __init__(self, exp, op):
        self.type = 'uop'
        self.exp = exp
        self.op = op

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: uop\n'
        res = res + prefix + 'op: ' + self.op + '\n'
        res = res + prefix + 'exp:\n'
        prefix = prefix + ' '
        res = res + self.exp.yaml_format(prefix)
        return res

class Lit:
    def __init__(self, value):
        self.type = 'lit'
        self.value = value

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: lit\n'
        res = res + prefix + 'value: ' + self.value + '\n'
        return res

class Tdecls:
    def __init__(self, typename):
        self.type = 'tdecls'
        self.types = []
        self.types.append(typename)

    def addType(self, typename):
        self.types.append(typename)

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: tdecls\n'
        res = res + prefix + 'types:\n'
        prefix = prefix + ' '
        for i in range(0, len(self.types)):
            res = res + prefix + '- ' + self.types[i].value + '\n'
        return res

class Vdecls:
    def __init__(self, vdecl):
        self.type = 'vdecls'
        self.vars = []
        self.vars.append(vdecl)
    
    def addVar(self, vdecl):
        self.vars.append(vdecl)

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: vdecls\n'
        res = res + 'vars:\n'
        prefix = prefix + ' '
        for i in range(0, len(self.vars)):
            res = res + prefix + '-\n'
            res  = res + self.vars[i].yaml_format(prefix + ' ')
        return res

class Vdecl:
    def __init__(self, typename, var):
        self.type = 'vdecl'
        self.typename = typename
        self.var = var

    def yaml_format(self, prefix = ''):
        res = prefix + 'node: vdecl\n' 
        res = res + self.typename.yaml_format(prefix) + self.var.yaml_format(prefix)
        return res

class Varid:
    def __init__(self, value):
        self.type = 'varid'
        self.value = value
    
    def yaml_format(self, prefix = ''):
        res = prefix + 'var: ' + self.value + '\n'
        return res

class GlobalID:
    def __init__(self, value):
        self.type = 'globid'
        self.value = value

    def yaml_format(self, prefix = ''):
        res = prefix + 'globid: ' + self.value + '\n'
        return res

class Type:
    def __init__(self, value):
        self.type = 'type'
        self.value = value

    def yaml_format(self, prefix = ''):
        res = prefix + 'type: ' + self.value + '\n'
        return res


### funcs ###
def p_exps(p):
    '''EXPS : EXP
            | EXP COMMA EXPS'''
    if len(p) == 2:
        p[0] = Exps(p[1])
    elif len(p) == 4:
        p[3].addExp(p[1]) 
        p[0] = p[3]

def p_exp(p):
    '''EXP : EXPPAREN
            | BINOP
            | UOP
            | LIT
            | VARID
            | EXPGLOBID'''
    p[0] = Exp(p[1])

def p_expParen(p):
    '''EXPPAREN : LPAREN EXP RPAREN'''
    p[0] = ExpParen(p[2])

def p_expGlobid(p):
    '''EXPGLOBID : GLOBID EXPWRAPPER'''
    p[0] = ExpGlobID(p[1].value, p[2])

def p_expWrapper(p):
    '''EXPWRAPPER : LPAREN RPAREN
                | LPAREN EXPS RPAREN'''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = None

def p_assign(p):
    '''ASSIGN : VARID EQUAL EXP'''
    p[0] = Assign(p[1], p[3])

def p_typeCast(p):
    '''TYPECAST : LBRACKET TYPE RBRACKET EXP'''
    p[0] = TypeCast(p[2], p[4])

def p_binop(p):
    '''BINOP : ARITHOPS
            | LOGICOPS
            | ASSIGN
            | TYPECAST'''
    p[0] = Binop(p[1])

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

def p_uop(p):
    '''UOP : NOT EXP
            | MINUS EXP'''
    if p[1] == '-':
        p[0] = Uop(p[2], 'minus')
    elif p[1] == '!':
        p[0] = Uop(p[2], 'not')
        
def p_lit(p):
    '''LIT : TRUE
            | FALSE
            | NUMBER'''
    p[0] = Lit(p[1])

def p_tdecls(p):
    '''TDECLS : TYPE
                | TYPE COMMA TDECLS'''
    if len(p) == 2:
        p[0] = Tdecls(p[1])
    else :
        p[3].addType(p[1])
        p[0] = p[3]

def p_vdecls(p):
    '''VDECLS : VDECL COMMA VDECLS
            | VDECL'''
    
    if len(p) == 4:
        p[3].addVar(p[1])
        p[0] = p[3]
    else:
        p[0] = Vdecls(p[1])


def p_vdecl(p):
    '''VDECL : TYPE VARID'''
    p[0] = Vdecl(p[1], p[2])


def p_varid(p):
    '''VARID : DOLLAR ID'''
    value = p[1] + p[2]
    p[0] = Varid(value)

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

def p_globid(p):
    '''GLOBID : ID'''
    p[0] = GlobalID(p[1])



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
$x = [int] ($a + $b - $c / $a * $b),($xyz > -$xy && $a < $b || ($c == $a || $x == 0))
'''

def p_error(p):
    print(f"Syntax error")

yacc.yacc(start = 'EXPS')
ast = yacc.parse(data, debug = False)
print(ast.yaml_format())
