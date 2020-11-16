import parser
import ply.yacc as yacc
import sys
from llvmlite import ir, binding
from externs import ExternalFunctions
import argparse

# flags = ['-h', '-?', '-v', '-O', '-emit-ast', '-emit-llvm', '-o', '-jit', '-o exe']

# args = sys.argv[1:]
# input_file_name = ''
# output_file_name = ''
# print_ir = False
# output_ast = False
# compile_jit = False

# for i in range(len(args)):
#     arg = args[i]

#     if i == len(args) - 1:
#         if arg in flags or args[i - 1] == '-o':
#             print('error: input file has not been specified.')
#             sys.exit(4)
#         else:
#             input_file_name = arg
#             break

#     if args[i - 1] == '-o':
#         continue

#     if arg not in flags:
#         print('error: flag ' + arg + ' is not a valid flag.')
#         sys.exit(1)

#     if arg == '-h' or arg == '-?':
#         print('''
#             -h or -? produce some help/usage message and the names of the authors. 
#             -v puts the compiler is "verbose" mode where additional information may be produced to standard output (otherwise, for correct inputs, no additional output may be produced, except for lines beginning with the string "warning: ").
#             -O enables optimizations.
#             -emit-ast causes the output file to contain the serialized format for the AST
#             -emit-llvm will cause the LLVM IR to be produced (unoptimized, unless -O is provided).
#             -o <output-file> names the output file.
#             <input-file> names in input source code.
#             ''')
#         print('Authors: Yangjun Bie, Qieer Zhang')
#     elif arg == '-v':
#         print('-v not implement yet.')
#     elif arg == '-O':
#         print('-O not implement yet.')
#     elif arg == '-emit-llvm':
#         print_ir = True
#     elif arg == '-emit-ast':
#         output_ast = True
#     elif arg == '-o':
#         if i == len(args) - 1 or args[i + 1] in flags:
#             print('error: output file has not been specified.')
#             sys.exit(3)
#         output_file_name = args[i + 1]
#     elif arg == '-jit':
#         compile_jit = True

# try:
#     with open(input_file_name, 'r') as file:
#         data = file.read()
# except IOError:
#     print('error: input file does not exist.')
#     sys.exit(5)

parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='input_file')
parser.add_argument('-emit-ast', action='store_true', default=False, dest='output_ast'),
parser.add_argument('-emit-llvm', action='store_true', default=False, dest='print_ir')
parser.add_argument('-jit', action='store_true', default=False, dest='compile_jit'),
parser.add_argument('-o', action='store', dest='output_file', required=False)
parser.add_argument('sysarg', nargs='*')
args = parser.parse_args()

try:
    with open(args.input_file, 'r') as file:
        data = file.read()
except IOError:
    print('error: input file does not exist.')
    sys.exit(5)

module = ir.Module(name=__file__)
external_funcs = ExternalFunctions(module, sys.argv)

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
    engine.run_static_constructors()

