import ply.yacc as yacc

from lexer import tokens

class Progress:
    def __init__(self, funcs, externs=[]):
        self.type = 'progress'
        self.funcs = Functions(funcs)
        self.externs = Externals(externs)

    def add_func(self, func):
        self.funcs.add(func)

    def add_extern(self, extern):
        self.externs.add(extern)

    def __repr__(self):
        res = 'name: prog\n'
        res = res + '  funcs:\n'
        res = res + self.funcs.yaml_format('    ')

        if self.externs.externs:
            res = res + '  externs:\n'
            res = res + self.externs.yaml_format('    ')

        return res

class Function:
    type = 'function'
    def __init__(self, ret_type, globid, blk, vdecls=None):
        self.ret_type = ret_type
        self.globid = globid
        self.blk = blk
        self.vdecls = vdecls

    def yaml_format(self, prefix=''):
        res = prefix + 'name: func\n'
        res = res + prefix + 'ret_type: ' + self.ret_type + '\n'
        res = res + prefix + 'globid: ' + self.globid + '\n'
        res = res + prefix + 'blk:\n'
        res = res + self.blk.yaml_format(prefix + '  ')
        if self.vdecls:
            res = res + prefix + 'vdecls:\n'
            res = res + self.vdecls.yaml_format(prefix + '  ')
        return res

class Functions:
    def __init__(self, functions):
        self.type = 'functions'
        self.functions = functions

    def add(self, func):
        self.functions.append(func)

    def yaml_format(self, prefix=''):
        res = prefix + 'name: funcs\n'
        res = res + prefix + 'funcs:\n'
        for func in self.functions:
            res = res + prefix + '  '+ '-\n'
            res = res + func.yaml_format(prefix + '    ')
        return res

class External:
    type = 'external'
    def __init__(self, ret_type, globid, tdecls=None):
        self.ret_type = ret_type
        self.globid = globid
        self.tdecls = tdecls

    def yaml_format(self, prefix=''):
        res = prefix + 'name: extern\n'
        res = res + prefix + 'ret_type: ' + self.ret_type + '\n'
        res = res + prefix + 'globid: ' + self.globid + '\n'
        if self.tdecls:
            res = res + prefix + 'tdecls:\n'
            res = res + self.tdecls.yaml_format(prefix + '  ')
        return res

class Externals:
    def __init__(self, externs):
        self.type = 'externs'
        self.externs = externs

    def add(self, extern):
        self.externs.append(extern)

    def yaml_format(self, prefix=''):
        res = prefix + 'name: externs\n'
        res = res + prefix + 'externs:\n'

        for extern in self.externs:
            res = res + prefix + '  '+ '-\n'
            res = res + extern.yaml_format(prefix + '    ')
        return res

class Blk:
    def __init__(self, stmts=[]):
        self.stmts = Statements(stmts)

    def yaml_format(self, prefix):
        res = prefix + 'name: blk\n'
        if self.stmts.stmts:
            res = res + prefix + 'contents:\n'
            res = res + self.stmts.yaml_format(prefix + '  ')
        return res

class Statements:
    def __init__(self, stmts=[]):
        self.stmts = stmts

    def yaml_format(self, prefix):
        res = prefix + 'name: stmts\n'
        res = res + prefix + 'stmts:\n'
        for stmt in self.stmts:
            res = res + prefix + '  ' + '-\n'
            res = res + stmt.yaml_format(prefix + '    ')
        return res

class BlkStatement:
    def __init__(self, blk):
        self.blk = blk 

    def yaml_format(self, prefix):
        res = prefix + 'name: blk\n'
        res = res + prefix + 'blk:\n'
        res = res + self.blk.yaml_format(prefix + '  ')
        return res

class ReturnStatement:
    def __init__(self, exp=None):
        self.exp = exp

    def yaml_format(self, prefix):
        res = prefix + 'name: ret\n'

        if self.exp:
            res = res + prefix + 'exp:\n'
            res = res + self.exp.yaml_format(prefix + '  ')

        return res

class VDeclStatement:
    def __init__(self, vdecl, exp):
        self.vdecl = vdecl
        self.exp = exp 

    def yaml_format(self, prefix):
        res = prefix + 'name: vardeclstmt\n'
        res = res + prefix + 'vdecl:\n'
        res = res + self.vdecl.yaml_format(prefix + '  ')
        res = res + prefix + 'exp:\n'
        res = res + self.exp.yaml_format(prefix + '  ')
        return res

class ExpSemiStatement:
    def __init__(self, exp):
        self.exp = exp 

    def yaml_format(self, prefix):
        res = prefix + 'name: expstmt\n'
        res = res + prefix + 'exp:\n'
        res = res + self.exp.yaml_format(prefix + '  ')
        return res

class WhileStatement:
    def __init__(self, exp, stmt):
        self.exp = exp 
        self.stmt = stmt 

    def yaml_format(self, prefix):
        res = prefix + 'name: while\n'
        res = res + prefix + 'cond:\n'
        res = res + self.exp.yaml_format(prefix + '  ')
        res = res + prefix + 'stmt:\n'
        res = res + self.stmt.yaml_format(prefix + '  ')
        return res

class IfStatement:
    def __init__(self, exp, stmt1, stmt2=None):
        self.exp = exp
        self.stmt1 = stmt1
        self.stmt2 = stmt2

    def yaml_format(self, prefix):
        res = prefix + 'name: if\n'
        res = res + prefix + 'cond:\n'
        res = res + self.exp.yaml_format(prefix + '  ')
        res = res + prefix + 'stmt:\n'
        res = res + self.stmt1.yaml_format(prefix + '  ')
        if self.stmt2:
            res = res + prefix + 'else_stmt:\n'
            res = res + self.stmt2.yaml_format(prefix + '  ')
        return res 

class PrintExpStatement:
    def __init__(self, exp):
        self.exp = exp 

    def yaml_format(self, prefix):
        res = prefix + 'name: print\n'
        res = res + prefix + 'exp:\n'
        res = res + self.exp.yaml_format(prefix + '  ')
        return res

class PrintSLitStatement:
    def __init__(self, slit):
        self.slit = slit 

    def yaml_format(self, prefix):
        res = prefix + 'name: printslit\n'
        res = res + prefix + 'string: ' + self.slit + '\n'
        return res

class Exps:
    def __init__(self, exp):
        self.exps = []
        self.exps.append(exp)

    def addExp(self, exp):
        self.exps.append(exp)

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: exps\n'
        res = res + prefix + 'exps:\n'
        prefix = prefix + ' '
        for i in range(0, len(self.exps)):
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
        res = res + prefix + 'vars:\n'
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
def p_prog(p):
    """
    PROG : FUNCS
        | EXTERNS FUNCS
    """
    if len(p) == 2:
        p[0] = Progress(p[1])
    else:
        p[0] = Progress(p[2], p[1])

def p_externs(p):
    '''
    EXTERNS : EXTERNSTS 
            | EXTERNS EXTERNSTS
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_funcs(p):
    '''
    FUNCS : FUNC
        | FUNCS FUNC
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_extern(p):
    '''
    EXTERNSTS : EXTERN TYPE ID LPAREN RPAREN SEMICOLON
            | EXTERN TYPE ID LPAREN TDECLS RPAREN SEMICOLON
    '''
    if len(p) == 7:
        p[0] = External(p[2].value, p[3])
    else:
        p[0] = External(p[2].value, p[3], p[5])

def p_func(p):
    '''
    FUNC : DEF TYPE ID LPAREN RPAREN BLK
    FUNC : DEF TYPE ID LPAREN VDECLS RPAREN BLK
    '''
    if len(p) == 7:
        p[0] = Function(p[2].value, p[3], p[6])
    else:
        p[0] = Function(p[2].value, p[3], p[7], p[5])

def p_blk(p):
    '''
    BLK : LBRACE RBRACE
    BLK : LBRACE STMTS RBRACE
    '''
    if len(p) == 3:
        p[0] = Blk()
    else:
        #print(p[2])
        p[0] = Blk(p[2])

def p_stmts(p):
    '''
    STMTS : STMT
    STMTS : STMTS STMT
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_stmt_blk(p):
    'STMT : BLK'
    p[0] = BlkStatement(p[1])

def p_stmt_ret(p):
    '''
    STMT : RETURN SEMICOLON 
         | RETURN EXP SEMICOLON
    '''
    if len(p) == 3:
        p[0] = ReturnStatement()
    else:
        p[0] = ReturnStatement(p[2])

def p_stmt_vdecl(p):
    '''
    STMT : VDECL EQUAL EXP SEMICOLON
    '''
    # need to modify vdecl and exp
    p[0] = VDeclStatement(p[1], p[3])

def p_stmt_expSemi(p):
    '''
    STMT : EXP SEMICOLON
    '''
    p[0] = ExpSemiStatement(p[1])

def p_stmt_while(p):
    '''
    STMT : WHILE LPAREN EXP RPAREN STMT
    '''
    p[0] = WhileStatement(p[3], p[5])

def p_stmt_if(p):
    '''
    STMT : IF LPAREN EXP RPAREN STMT
         | IF LPAREN EXP RPAREN STMT ELSE STMT
    '''
    if len(p) == 6:
        p[0] = IfStatement(p[3], p[5])
    else:
        p[0] = IfStatement(p[3], p[5], p[7])

def p_stmt_print_exp(p):
    '''
    STMT : PRINT EXP SEMICOLON
    '''
    p[0] = PrintExpStatement(p[2])

def p_stmt_print_slit(p):
    '''
    STMT : PRINT SLIT SEMICOLON
    '''
    p[0] = PrintSLitStatement(p[2])

def p_exps(p):
    '''EXPS : EXP
            | EXPS COMMA EXP'''
    if len(p) == 2:
        p[0] = Exps(p[1])
    elif len(p) == 4:
        p[1].addExp(p[3]) 
        p[0] = p[1]

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
                | TDECLS COMMA TYPE'''
    if len(p) == 2:
        p[0] = Tdecls(p[1])
    else :
        p[1].addType(p[3])
        p[0] = p[1]

def p_vdecls(p):
    '''VDECLS : VDECLS COMMA VDECL
            | VDECL'''
    
    if len(p) == 4:
        p[1].addVar(p[3])
        p[0] = p[1]
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

def p_error(p):
    print(f"Syntax error")



precedence = (
    ('right', 'COMMA'),
    ('right', 'EQUAL'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALITY'),
    ('left', 'LESS', 'GREATER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES','DIVIDE'),
)

yacc.yacc()
