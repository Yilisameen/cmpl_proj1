import ply.yacc as yacc

from lexer import tokens

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


data = '''
int
'''

yacc.yacc(start = 'TDECLS')
ast = yacc.parse(data, debug = False)
ast.yaml()
