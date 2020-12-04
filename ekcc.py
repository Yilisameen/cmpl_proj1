import parser
import ply.yacc as yacc
import sys
from llvmlite import ir, binding
from externs import ExternalFunctions
import argparse
from ctypes import *
try:
    from time import perf_counter as time
except ImportError:
    from time import time

parser = argparse.ArgumentParser()
parser.add_argument('input_file', metavar='input_file', help='the name of the input file your want to parse')
parser.add_argument('-emit-ast', action='store_true', default=False, dest='output_ast', help='to save the ast into the output file'),
parser.add_argument('-emit-llvm', action='store_true', default=False, dest='print_ir', help="to print intermediate representation to the console")
parser.add_argument('-jit', action='store_true', default=False, dest='compile_jit', help="to compile, jit and run the code"),
parser.add_argument('-O', action='store_true', default=False, dest='optimized', help="to optimized the code")
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

    # target = binding.Target.from_default_triple()
    # target_machine = target.create_target_machine()

    # backing_mod = binding.parse_assembly("")
    # engine = binding.create_mcjit_compiler(backing_mod, target_machine)
    
    ir = str(module)
    mod = binding.parse_assembly(ir)
    mod.verify()

    #optimize the code
    if args.optimized:
        pmb = binding.PassManagerBuilder()
        pmb.opt_level = 0
        fpm = binding.create_function_pass_manager(mod)
        pmb.populate(fpm)
        pm = binding.ModulePassManager()
        pmb.populate(pm)

        # pm.add_constant_merge_pass()
        # pm.add_dead_arg_elimination_pass()
        # pm.add_function_attrs_pass()
        # pm.add_function_inlining_pass(200) # threshold = 200
        # pm.add_global_dce_pass()
        # pm.add_global_optimizer_pass()
        # pm.add_ipsccp_pass()
        # pm.add_dead_code_elimination_pass()
        # pm.add_cfg_simplification_pass()   
        # pm.add_gvn_pass()
        pm.add_instruction_combining_pass()
        # pm.add_licm_pass()
        # pm.add_sccp_pass()
        # pm.add_sroa_pass()
        # pm.add_type_based_alias_analysis_pass()
        pm.add_basic_alias_analysis_pass()

        t1 = time()

        pm.run(mod)

        t2 = time()

        print("optimize time: ", t2 - t1)
    #### optimized end ####

    t3 = time()

    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()

    with binding.create_mcjit_compiler(mod, target_machine) as engine:
	    # engine.add_module(mod)
	    engine.finalize_object()
	    entry = engine.get_function_address("main")

	    t4 = time()
	    print("JIT compile time: ", t4 - t3)

	    t5 = time()

	    cfunc = CFUNCTYPE(c_int)(entry)
	    result = cfunc()

	    t6 = time()
	    print("Execution of the program: ", t6 - t5)

	    print("program result:{}".format(result))
	    print(mod)

