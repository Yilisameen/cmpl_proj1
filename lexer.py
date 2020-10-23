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
    'noalias': 'NOALIAS'
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
    def __init__(self, funcs, externs=None):
        self.funcs = funcs

        if externs:
            self.externs = externs
        else:
            self.externs = None

    def yaml_format(self):
        res = 'names: prog\n'
        res = res + '  funcs:\n'
        res = res + self.funcs.yaml_format('    ')

        if self.externs:
            res = res + '  externs:\n'
            res = res + self.externs.yaml_format('    ')

        return res

class Function:
    type = 'function'
    def __init__(self, ret_type, globid):
        self.ret_type = ret_type
        self.globid = globid

    def yaml_format(self, prefix=''):
        res = prefix + '-\n'
        res = res + prefix + '  ' + 'name: func\n'
        res = res + prefix + '  ' + 'ret_type:' + self.ret_type + '\n'
        res = res + prefix + '  ' + 'globid: ' + self.globid + '\n'
        return res

class Functions:
    def __init__(self, functions):
        self.functions = functions

    def yaml_format(self, prefix=''):
        res = prefix + 'name: funcs\n'
        res = res + prefix + 'funcs:\n'

        for func in self.functions:
            res = res + func.yaml_format(prefix + '  ')
        return res

class External:
    type = 'external'
    def __init__(self, ret_type, globid):
        self.ret_type = ret_type
        self.globid = globid

    def yaml_format(self, prefix=''):
        res = prefix + '-\n'
        res = res + prefix + '  ' + 'name: extern\n'
        res = res + prefix + '  ' + 'ret_type:' + self.ret_type + '\n'
        res = res + prefix + '  ' + 'globid: ' + self.globid + '\n'
        return res

class Externals:
    def __init__(self, externs):
        self.externs = externs

    def yaml_format(self, prefix=''):
        res = prefix + 'name: externs\n'
        res = res + prefix + 'externs:\n'

        for extern in self.externs:
            res = res + extern.yaml_format(prefix + '  ')
        return res

def p_prog(p):
    """
    prog : funcs
    prog : externs funcs
    prog : funcs externs
    """
    if len(p) == 2:
        p[0] = Progress(Functions(p[1]))
    elif len(p) == 3:
        if p[1][0].type == 'function':
            p[0] = Progress(Functions(p[1]), Externals(p[2]))
        else:
            p[0] = Progress(Functions(p[2]), Externals(p[1]))
    print(p[0].yaml_format())

def p_funcs(p):
    """
    funcs : func
    funcs : funcs func
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]

def p_externs(p):
    """
    externs : extern
    externs : externs extern
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]

def p_extern(p):
    'extern : EXTERN INT'
    p[0] = External(p[2], 'test')

def p_func(p):
    'func : DEF INT'
    p[0] = Function(p[2], 'test_f')

def p_error(p):
    print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('input > ')
    except EOFError:
        break
    yacc.parse(s)
