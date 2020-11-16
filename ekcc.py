import parser
import ply.yacc as yacc
import sys
from llvmlite import ir, binding
from externs import ExternalFunctions
import argparse
from ctypes import *

parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='input_file', help='the name of the input file your want to parse')
parser.add_argument('-emit-ast', action='store_true', default=False, dest='output_ast', help='to save the ast into the output file'),
parser.add_argument('-emit-llvm', action='store_true', default=False, dest='print_ir', help="to print intermediate representation to the console")
parser.add_argument('-jit', action='store_true', default=False, dest='compile_jit', help="to compile, jit and run the code"),
parser.add_argument('-o', action='store', dest='output_file', required=False, help='the name of the output file to store ast')
parser.add_argument('-sysarg', nargs='*', help="system arguments for the input code")
args = parser.parse_args()

try:
    with open(args.input_file, 'r') as file:
        data = file.read()
except IOError:
    print('error: input file does not exist.')
    sys.exit(5)

module = ir.Module(name=__file__)
external_funcs = ExternalFunctions(module, args.sysarg[1:])

parse_result = yacc.parse(data, debug = False)
parse_result.eval(module, external_funcs)

# print ir to the console
if args.print_ir:
    print(module)

# save ast to the output file
ast = ""
if args.output_ast:
    ast = parse_result.yaml_format()

    with open(args.output_file, 'w') as file:
        file.write('---\n')
        file.write(ast)
        file.write('...\n')

# compile, jit and run the code
if args.compile_jit:
    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()

    backing_mod = binding.parse_assembly("")
    engine = binding.create_mcjit_compiler(backing_mod, target_machine)
    
    ir = str(module)
    mod = binding.parse_assembly(ir)
    mod.verify()
    engine.add_module(mod)
    engine.finalize_object()
    entry = engine.get_function_address("main")
    cfunc = CFUNCTYPE(c_int)(entry)
    result = cfunc()
    print("program result:{}".format(result))

