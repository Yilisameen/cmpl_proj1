import ply.lex as lex

# List of token names.   This is always required
reserved = {
    'extern' : "EXTERN",
    'def' : 'DEF',
    'return' : 'RETURN',
    'while' : 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'print' : 'PRINT',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'int' : 'INT',
    'cint' : 'CINT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'void' : 'VOID',
    'ref' : 'REF',
    'noalias': 'NOALIAS',
    'tdecls' : 'tdecls',
    'vdecls' : 'vdecls',
    'vdecl' : 'vdecl',
    'exp' : 'exp'
}

tokens = [
        'EQUALITY', 'AND', 'OR',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
        'NOT', 'COMMA', 'SEMICOLON', 'EQUAL', 'LESS', 'GREATER', 'DOLLAR',
        'NUMBER', 'ID', 'SLIT', ] + list(reserved.values())

# Regular expression rules for simple tokens
t_EQUALITY = r'=='
t_AND = r'&&'
t_OR = r'\|\|'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_NOT = r'!'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUAL = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_DOLLAR = r'\$'
t_NUMBER = r'[0-9]+(\.[0-9]+)?'
t_SLIT = r'"[^"\n\r]*"'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
# Ignore comments
t_ignore_COMMENT = r'\#.*'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

###############################################################################
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
        res = 'names: prog\n'
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


########################################### test classes ############
class TDecls:
    def __int__(self, tdecls=[]):
        self.tdecls = tdecls

    def yaml_format(self, prefix):
        res = prefix + 'names: tdecls\n'
        res = res + prefix + '11111111\n'
        res = res + prefix + '11111111\n'
        res = res + prefix + '11111111\n'
        return res

class VDecls:
    def __int__(self, vdecls=[]):
        self.vdecls = vdecls

    def yaml_format(self, prefix):
        res = prefix + 'names: vdecls\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'
        return res

class VDecl:
    def __init__(self):
        self.vdecl = ''

    def yaml_format(self, prefix):
        res = prefix + 'names: vdecl\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'
        return res

class Expression:
    def __int__(self, exp=None):
        self.exp = exp

    def yaml_format(self, prefix):
        res = prefix + 'names: exp\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'
        return res

class Expressions:
    def __int__(self, exps=None):
        self.exps = exps

    def yaml_format(self, prefix):
        res = prefix + 'names: exps\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'
        res = res + prefix + '22222222\n'


########################################################################

def p_prog(p):
    """
    prog : funcs
    prog : externs funcs
    """
    if len(p) == 2:
        p[0] = Progress(p[1])
    else:
        p[0] = Progress(p[2], p[1])

def p_externs(p):
    '''
    externs : extern 
    externs : extern externs
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[2].append(p[1])
        p[0] = p[2]


def p_funcs(p):
    '''
    funcs : func
    funcs : func funcs
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[2].append(p[1])
        p[0] = p[2]

def p_extern(p):
    '''
    extern : EXTERN TYPE ID LPAREN RPAREN SEMICOLON
    extern : EXTERN TYPE ID LPAREN tdecls RPAREN SEMICOLON
    '''
    if len(p) == 7:
        p[0] = External(p[2], p[3])
    else:
        p[0] = External(p[2], p[3], TDecls())

def p_func(p):
    '''
    func : DEF TYPE ID LPAREN RPAREN blk
    func : DEF TYPE ID LPAREN vdecls RPAREN blk
    '''
    if len(p) == 7:
        p[0] = Function(p[2], p[3], p[6])
    else:
        p[0] = Function(p[2], p[3], p[7], VDecls())

def p_blk(p):
    '''
    blk : LBRACE RBRACE
    blk : LBRACE stmts RBRACE
    '''
    if len(p) == 3:
        p[0] = Blk()
    else:
        print(p[2])
        p[0] = Blk(p[2])

def p_stmts(p):
    '''
    stmts : stmt
    stmts : stmt stmts
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[2].append(p[1])
        p[0] = p[2]

def p_stmt_blk(p):
    'stmt : blk'
    p[0] = BlkStatement(p[1])

def p_stmt_ret(p):
    '''
    stmt : RETURN SEMICOLON 
         | RETURN exp SEMICOLON
    '''
    if len(p) == 3:
        p[0] = ReturnStatement()
    else:
        p[0] = ReturnStatement(Expression())

def p_stmt_vdecl(p):
    '''
    stmt : vdecl EQUAL exp SEMICOLON
    '''
    # need to modify vdecl and exp
    p[0] = VDeclStatement(VDecl(), Expression())

def p_stmt_expSemi(p):
    '''
    stmt : exp SEMICOLON
    '''
    p[0] = ExpSemiStatement(Expression())

def p_stmt_while(p):
    '''
    stmt : WHILE LPAREN exp RPAREN stmt
    '''
    p[0] = WhileStatement(Expression(), p[5])

def p_stmt_if(p):
    '''
    stmt : IF LPAREN exp RPAREN stmt
         | IF LPAREN exp RPAREN stmt ELSE stmt
    '''
    if len(p) == 6:
        p[0] = IfStatement(Expression(), p[5])
    else:
        p[0] = IfStatement(Expression(), p[5], p[7])

def p_stmt_print_exp(p):
    '''
    stmt : PRINT exp SEMICOLON
    '''
    p[0] = PrintExpStatement(Expression())

def p_stmt_print_slit(p):
    '''
    stmt : PRINT SLIT SEMICOLON
    '''
    p[0] = PrintSLitStatement(p[2])

############################## test functions #############################
def p_type(p):
    '''
    TYPE : INT
         | CINT
         | FLOAT
         | BOOL 
         | VOID
    '''
    p[0] = p[1]

###########################################################################

def p_error(p):
    print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('input > ')
    except EOFError:
        break
    print(yacc.parse(s))
