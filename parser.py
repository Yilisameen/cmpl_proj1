import ply.yacc as yacc
import sys, traceback

from lexer import tokens
from llvmlite import ir

class Progress:
    def __init__(self, funcs, externs=[]):
        self.type = 'progress'
        self.funcs = Functions(funcs)
        self.externs = Externals(externs)

    def add_func(self, func):
        self.funcs.add(func)

    def add_extern(self, extern):
        self.externs.add(extern)

    def yaml_format(self):
        res = 'name: prog\n'
        res = res + 'funcs:\n'
        res = res + self.funcs.yaml_format('  ')

        if self.externs.externs:
            res = res + 'externs:\n'
            res = res + self.externs.yaml_format('  ')

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
        res = self.blk.yaml_format(prefix)
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
        if vdecl.is_ref and exp.exp.type != 'varid':
            try:
                raise Exception()
            except:
                print('error: ref var initializer must be a variable.')
                sys.exit(10)
        
        self.vdecl = vdecl
        self.exp = exp

    def node_type_check(self):
        global ref_type_map
        left_type = ref_type_map.get(self.vdecl.typename.value, self.vdecl.typename.value)
        right_type = ref_type_map.get(self.exp.get_type(), self.exp.get_type())
        if left_type != right_type:
            try:
                raise Exception()
            except:
                print('error: Relevant AST 10 nodes don\'t have the correct type.')
                sys.exit(12)
        return True
            

    def yaml_format(self, prefix = ''):
        if not self.node_type_check():
            try:
                raise Exception()
            except:
                print('error: Relevant AST 11 nodes don\'t have the correct type.')
                sys.exit(12)
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
        prefix = prefix + '  '
        for i in range(0, len(self.exps)):
            res = res + prefix + '-\n'
            res = res + self.exps[i].yaml_format(prefix + '  ')
        return res

    def eval(self, module, builder):
        for exp in self.exps:
            exp.eval(module, builder)

class Exp:
    def __init__(self, exp):
        self.type = 'exp'
        self.exp = exp

    def get_type(self):
        return self.exp.get_type()

    def yaml_format(self, prefix = ''):
        res = ''
        if self.exp.type != 'expParen':
            res = prefix + 'binop_type: ' + self.exp.get_type() + '\n'
        if self.exp.type == 'varid':
            res = res + prefix + 'name: varval\n'
        if self.exp.type == 'expGlobID' and self.exp.globid not in functions and self.exp.globid not in externals:
            try:
                raise Exception()
            except:
                print('error: all functions must be declared before use.')
                sys.exit(8)
        res = res + self.exp.yaml_format(prefix)
        return res

    def eval(self, module, builder):
        return self.exp.eval(module, builder)

class Binop:
    def __init__(self, value):
        self.type = 'binop'
        self.value = value

    def get_type(self):
        return self.value.get_type()

    def node_type_check(self):
        return self.value.node_type_check()
    
    def yaml_format(self, prefix = ''):
        is_valid = self.node_type_check()
        if not is_valid:
            try:
                raise Exception()
            except:
                print('error: Relevant AST 0 nodes don\'t have the correct type.')
                sys.exit(12)

        if self.value.type == 'typeCast':
            res = prefix + 'name: caststmt\n'
        elif self.value.type == 'assign':
            res = prefix + 'name: assign\n'
        # elif self.value.type == 'expGlobID':
        #     res = prefix + 'name: funccall\n'
        else:
            res = prefix + 'name: binop\n'
        res = res + self.value.yaml_format(prefix)
        return res

    def eval(self, module, builder):
        return self.value.eval(module, builder)

class ExpParen:
    def __init__(self, exp):
        self.type = 'expParen'
        self.exp = exp

    def get_type(self):
        return self.exp.get_type()
    
    def yaml_format(self, prefix = ''):
        return self.exp.yaml_format(prefix)

    def eval(self, module, builder):
        return self.exp.eval(module, builder)

globid_type = {}

class ExpGlobID:
    def __init__(self, globid, params):
        self.type = 'expGlobID'
        self.globid = globid
        self.params = params

    def get_type(self):
        global globid_type
        globId_type = globid_type.get(self.globid, None)
        if globId_type == None:
            try:
                raise Exception()
            except:
                print('errors: all functions must be declared before use')
                sys.exit(-1)
        return globId_type
    
    def yaml_format(self, prefix = ''):
        res = prefix + 'name: funccall\n'
        res = res + prefix + 'globid: ' + self.globid + '\n'
        if self.params is not None:
            res = res + prefix + 'params: \n'
            res = res + self.params.yaml_format(prefix + '  ')
        return res

class Assign:
    def __init__(self, var, exp):
        self.type = 'assign'
        self.var = var
        self.exp = exp
    
    def get_type(self):
        if self.node_type_check():
            return self.exp.get_type()
        else:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)

    def node_type_check(self):
        global varid_type
        var_type = ref_type_map.get(self.var.get_type(), self.var.get_type())
        exp_type = ref_type_map.get(self.exp.get_type(), self.exp.get_type())
        if var_type != exp_type:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)
        else:
            return True

    def yaml_format(self, prefix = ''):
        res = self.var.yaml_format(prefix)
        res = res + prefix + 'exp:\n'
        res = res + self.exp.yaml_format(prefix + '  ')
        return res
    
    def eval(self, module, builder): # not tested yet
        var_name = self.var.value
        print(var_name)
        ptr = varid_symbol_ptr_table.get(var_name, None)
        if ptr == None:
            raise Exception()
        value = self.exp.eval(module, builder)
        if value.type.is_pointer:
            value = builder.load(value)
        if ptr.type.pointee == ir.IntType(32):
            if value.type == ir.IntType(1):
                value = builder.uitofp(value, ir.FloatType())
            if value.type == ir.FloatType():
                value = builder.fptosi(value, ptr.type.pointee)
        elif ptr.type.pointee == ir.FloatType(32):
            if value.type == ir.IntType(1) or value.type == ir.IntType(32):
                value = builder.uitofp(value, ir.FloatType())

        builder.store(value, ptr)
        return None

cast_list = ['int', 'cint', 'float']

class TypeCast:
    def __init__(self, typename, exp):
        self.type = 'typeCast'
        self.typename = typename
        self.exp = exp

    def get_type(self):
        if self.node_type_check():
            return self.typename.value
        else:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)
    
    def node_type_check(self):
        exp_type = self.exp.get_type()
        global cast_list
        if exp_type in cast_list and self.typename.value in cast_list:
            return True
        elif exp_type == 'bool' and self.typename.value == 'bool':
            return True
        else:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)

    def yaml_format(self, prefix = ''):
        res = self.typename.yaml_format(prefix)
        res = res + prefix + 'exp:\n'
        res = res + self.exp.yaml_format(prefix + '  ')
        return res

    def eval(self, module, builder):
        cast_to_type = self.typename.value
        cast_from_type = ref_type_map.get(self.exp.get_type(), self.exp.get_type())
        i_exp = self.exp.eval(module, builder)
        if cast_to_type == 'int' and cast_from_type == 'float':
            i = builder.fptosi(i_exp, ir.IntType(32))
        elif cast_to_type == 'float' and cast_from_type == 'int':
            i = builder.sitofp(i_exp, ir.FloatType())
        return i

ref_type_map = {
    'int': 'int',
    'ref int': 'int',
    'noalias ref int' : 'int',
    'cint': 'cint',
    'ref cint' : 'cint',
    'noalias ref cint' : 'cint',
    'float' : 'float',
    'ref float' : 'float',
    'noalias ref float' : 'float'
}

class ArithOps:
    def __init__(self, op, lhs, rhs):
        self.type = 'arithOps'
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def get_type(self):
        if self.node_type_check():
            return ref_type_map.get(self.lhs.get_type(), None)
        else:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)

    def node_type_check(self):
        global ref_type_map
        left_type = ref_type_map.get(self.lhs.get_type(), None)
        right_type = ref_type_map.get(self.rhs.get_type(), None)
        if left_type == right_type and left_type != None and right_type != None:
            return True
        else:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)
            

    def yaml_format(self, prefix = ''):
        res = prefix + 'op: ' + self.op + '\n'
        res = res + prefix + 'lhs: \n'
        res = res + self.lhs.yaml_format(prefix + '  ')
        res = res + prefix + 'rhs: \n'
        res = res + self.rhs.yaml_format(prefix + '  ')
        return res

    def eval(self, module, builder):
        value_type = self.get_type()
        i_lhs = self.lhs.eval(module, builder)
        i_rhs = self.rhs.eval(module, builder)
        if value_type == 'int':
            if self.op == 'add':
                i = builder.add(i_lhs, i_rhs)
            elif self.op == 'sub':
                i = builder.sub(i_lhs, i_rhs)
            elif self.op == 'mul':
                i = builder.mul(i_lhs, i_rhs)
            elif self.op == 'div':
                i = builder.sdiv(i_lhs, i_rhs)
        elif value_type == 'float':
            if self.op == 'add':
                i = builder.fadd(i_lhs, i_rhs)
            elif self.op == 'sub':
                i = builder.fsub(i_lhs, i_rhs)
            elif self.op == 'mul':
                i = builder.fmul(i_lhs, i_rhs)
            elif self.op == 'div':
                i = builder.fdiv(i_lhs, i_rhs)
        return i


class LogicOps:
    def __init__(self, op, lhs, rhs):
        self.type = 'logicOps'
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
    
    def get_type(self):
        if self.node_type_check():
            return 'bool'
        else:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)

    def node_type_check(self):
        if self.lhs.get_type() == 'bool' and self.rhs.get_type() == 'bool':
            if self.op == 'and' or self.op == 'or' or self.op == 'eq':
                return True
            else:
                try:
                    raise Exception()
                except:
                    print(self.op)
                    print('errors: Relevant AST 6nodes don\'t have the correct type')
                    sys.exit(12)
        left_type = ref_type_map.get(self.lhs.get_type(), None)
        right_type = ref_type_map.get(self.rhs.get_type(), None)
        if left_type != right_type and left_type != None and right_type != None:
            try:
                raise Exception()
            except:
                print('errors: Relevant AST nodes don\'t have the correct type')
                sys.exit(12)
        else:
            return True

    def yaml_format(self, prefix = ''):
        res = prefix + 'op: ' + self.op + '\n'
        res = res + prefix + 'lhs: \n'
        res = res + self.lhs.yaml_format(prefix + '  ')
        res = res + prefix + 'rhs: \n'
        res = res + self.rhs.yaml_format(prefix + '  ')
        return res

    def eval(self, module, builder):
        value_type = self.lhs.get_type()
        i_lhs = self.lhs.eval(module, builder)
        i_rhs = self.rhs.eval(module, builder)
        # print(value_type)
        # print(self.op)
        if value_type == 'int':
            if self.op == 'eq':
                i = builder.icmp_signed('==', i_lhs, i_rhs)
            elif self.op == 'gt':
                i = builder.icmp_signed('>', i_lhs, i_rhs)
            elif self.op =='lt':
                i = builder.icmp_signed('<', i_lhs, i_rhs)
        elif value_type == 'float':
            if self.op == 'eq':
                i = builder.fcmp_ordered('==', i_lhs, i_rhs)
            elif self.op == 'gt':
                i = builder.fcmp_ordered('>', i_lhs, i_rhs)
            elif self.op =='lt':
                i = builder.fcmp_ordered('<', i_lhs, i_rhs)
        elif value_type == 'bool':
            if self.op == 'eq':
                i = builder.fcmp_ordered('==', i_lhs, i_rhs)
            elif self.op == 'and':
                i = builder.and_(i_lhs, i_rhs)
            elif self.op == 'or':
                i = builder.or_(i_lhs, i_rhs)
        return i

class Uop:
    def __init__(self, exp, op):
        self.type = 'uop'
        self.exp = exp
        self.op = op

    def get_type(self):
        if self.op == 'not' and self.exp.get_type() != 'bool':
            try:
                raise Exception()
            except:
                print('errors: type of uop is not bool')
                sys.exit(-1)
        return 'bool'

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: uop\n'
        res = res + prefix + 'op: ' + self.op + '\n'
        res = res + prefix + 'exp:\n'
        prefix = prefix + '  '
        res = res + self.exp.yaml_format(prefix)
        return res
    
    def eval(self, module, builder):
        if self.op == 'not':
            i = builder.not_(self.exp.eval(module, builder))
        elif self.op == 'minus':
            i = builder.neg(self.exp.eval(module, builder))
        return i

class Lit:
    def __init__(self, value):
        self.type = 'lit'
        self.value = value

    def get_type(self):
        if self.value == 'true' or self.value ==  'false':
            return 'bool'
        elif '.' in self.value:
            return 'float'
        else:
            return 'int'

    def yaml_format(self, prefix = ''):
        res = prefix + 'name: lit\n'
        res = res + prefix + 'value: ' + self.value + '\n'
        return res

    def eval(self, builder, module):
        lit_type = self.get_type()
        # print(lit_type)
        if lit_type == 'bool':
            if self.value == 'true':
                i = ir.Constant(ir.IntType(1), 1)
            elif self.value == 'false':
                i = ir.Constant(ir.IntType(1), 0)
        elif lit_type == 'float':
            i = ir.Constant(ir.FloatType(), float(self.value))
        elif lit_type == 'int':
            i = ir.Constant(ir.IntType(32), int(self.value))
        return i

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
        prefix = prefix + '  '
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
        prefix = prefix + '  '
        for i in range(0, len(self.vars)):
            res = res + prefix + '-\n'
            res  = res + self.vars[i].yaml_format(prefix + '  ')
        return res

    def eval(self, module, builder):
        for vdecl in self.vars:
            vdecl.eval(module, builder)

class Vdecl:
    def __init__(self, typename, var, is_ref = False):
        self.type = 'vdecl'
        if typename.value == 'void':
            try:
                raise Exception()
            except:
                print('error: <vdecl> may not have void type.')
                sys.exit(6)
        self.typename = typename
        self.var = var
        self.is_ref = is_ref

    def yaml_format(self, prefix = ''):
        res = prefix + 'node: vdecl\n' 
        res = res + self.typename.yaml_format(prefix) + self.var.yaml_format(prefix)
        return res

    def eval(self, module, builder):
        var_type = self.typename.value
        var_name = self.var.value
        is_ref = self.is_ref
        print(var_type)
        print(var_name)
        if is_ref:
            if 'int' in var_type:
                var_ptr = builder.alloca(ir.PointerType(ir.IntType(32)))
            elif 'float' in var_type:
                var_ptr = builder.alloca(ir.PointerType(ir.FloatType()))
            elif 'bool' in var_type:
                var_ptr = builder.alloca(ir.PointerType(ir.IntType(1)))
        else:
            if var_type == 'int':
                var_ptr = builder.alloca(ir.IntType(32))
            elif var_type == 'float':
                var_ptr = builder.alloca(ir.FloatType())
            elif var_type == 'bool':
                var_ptr = builder.alloca(ir.IntType(1))
        varid_symbol_ptr_table[var_name] = var_ptr

    

varid_type = {}

class Varid:
    def __init__(self, value):
        self.type = 'varid'
        self.value = value

    def get_type(self):
        global varid_type
        var_type = varid_type.get(self.value, None)
        if var_type == None:
            try:
                raise Exception()
            except:
                print('errors: varid used before define')
                sys.exit(-1)
        else:
            return var_type
    
    def yaml_format(self, prefix = ''):
        res = prefix + 'var: ' + self.value + '\n'
        return res

    def eval(self, module, builder): # not tested yet
        var_name = self.value
        print(var_name)
        ptr = varid_symbol_ptr_table.get(var_name, None)
        if ptr == None:
            raise Exception()
        val = builder.load(ptr)
        return val


varid_symbol_ptr_table = {}   #varid_name : pointer


class GlobalID:
    def __init__(self, value):
        self.type = 'globid'
        self.value = value

    def yaml_format(self, prefix = ''):
        res = prefix + 'globid: ' + self.value + '\n'
        return res

class Type:
    def __init__(self, value, is_noalias = False, is_ref = False):
        self.type = 'type'
        self.is_noalias = is_noalias
        self.is_ref = is_ref
        self.value = value

    def yaml_format(self, prefix = ''):
        res = prefix + 'type: ' + self.value + '\n'
        return res

externals = []
functions = []
has_run_function = []

### funcs ###
def p_prog(p):
    """
    PROG : FUNCS
        | EXTERNS FUNCS
    """
    if not has_run_function:
            try:
                raise Exception()
            except:
                print('error: there is no function named "run" in the program.')
                sys.exit(11)

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
    externals.append(p[3])
    globid_type[p[3]] = p[2].value


def p_func(p):
    '''
    FUNC : DEF TYPE ID LPAREN RPAREN BLK
    FUNC : DEF TYPE ID LPAREN VDECLS RPAREN BLK
    '''
    if p[3] == 'run':
            if has_run_function:
                try:
                    raise Exception()
                except:
                    print('error: there cannot be over 1 functions named "run".')
                    sys.exit(11)
            if p[2].value != 'int':
                try:
                    raise Exception()
                except:
                    print('error: "run" function\'s return type must be "int".')
                    sys.exit(11)
            if len(p) != 7:
                try:
                    raise Exception()
                except:
                    print('error: "run" function should take no argument.')
                    sys.exit(11)
            has_run_function.append(1)
    
    if p[2].is_ref:
        try:
            raise Exception()
        except:
            print('error: a function may not return a ref type.')
            sys.exit(9)

    if len(p) == 7:
        p[0] = Function(p[2].value, p[3], p[6])
    else:
        p[0] = Function(p[2].value, p[3], p[7], p[5])
    functions.append(p[3])
    globid_type[p[3]] = p[2].value

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
        p[0] = ArithOps('mul', p[1], p[3])
    elif p[2] == '/':
        p[0] = ArithOps('div', p[1], p[3])
    elif p[2] == '+':
        p[0] = ArithOps('add', p[1], p[3])
    elif p[2] == '-':
        p[0] = ArithOps('sub', p[1], p[3])

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
    p[0] = Vdecl(p[1], p[2], p[1].is_ref)
    varid_type[p[2].value] = p[1].value


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
    if p[2].is_ref:
        try:
            raise Exception()
        except:
            print('error: a ref type may not contain a \'ref\' type.')
            sys.exit(7)
    if p[2].value == 'void':
        try:
            raise Exception()
        except:
            print('error: a ref type may not contain a \'void\' type.')
            sys.exit(7)
    value = 'ref ' + p[2].value
    p[0] = Type(value, False, True)

def p_refTypeNoAlias(p):
    '''TYPE : NOALIAS REF TYPE'''
    if p[3].is_ref:
        try:
            raise Exception()
        except:
            print('error: a ref type may not contain a \'ref\' type.')
            sys.exit(7)
    if p[3].value == 'void':
        try:
            raise Exception()
        except:
            print('error: a ref type may not contain a \'void\' type.')
            sys.exit(7)
    value = 'noalias ref ' + p[3].value
    p[0] = Type(value, True, True)

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

yacc.yacc(start='VDECLS')
