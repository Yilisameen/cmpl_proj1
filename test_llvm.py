# from llvmlite import ir

# # Create some useful types
# inttype = ir.IntType(32)
# fnty = ir.FunctionType(inttype, (inttype, inttype))
# # char_pointer = ir.IntType(8).as_pointer()
# fnty1 = ir.FunctionType(ir.VoidType(), [ir.IntType(32)], True)

# # Create an empty module...
# module = ir.Module(name=__file__)
# # and declare a function named "fpadd" inside it
# func = ir.Function(module, fnty, name="fpadd")

# # Now implement the function
# block = func.append_basic_block(name="entry")
# builder = ir.IRBuilder(block)
# a, b = func.args
# # result = builder.fadd(a, b, name = "res")
# test = builder.sadd_with_overflow(a, b, name = 'test')
# res = builder.extract_value(test, 0)
# bits = builder.extract_value(test, 1)
# cond = builder.not_(bits)
# builder.assume(ir.Constant(ir.IntType(1), 0))
# # with builder.if_else(bits) as (then, otherwise):
# #     with then:
# #         pass
# #     with otherwise:
# #         builder.
# # char_pointer = ir.IntType(8).as_pointer()
# # fnty1 = ir.FunctionType(ir.VoidType(), [char_pointer], True)

# # func = ir.Function(module, fnty1, name="printf")
# # builder = ir.IRBuilder(block)


# # builder.ret(result)

# # tst_fnty = ir.FunctionType(double, [])
# # func_tst = ir.Function(module, tst_fnty, name = "tst")
# # block = func.append_basic_block(name="entry")

# # func2 = ir.Function(module, fnty, name="fpsub")
# # block = func2.append_basic_block(name="entry")
# # builder = ir.IRBuilder(block)
# # a, b = func2.args
# # result1 = builder.call(func, [a, b])
# # builder.ret(result1)

# # a, b = func2.args
# # result = builder.fsub(a,b, name = "res")
# # builder.ret(result)

# # Print the module IR
# print(module)


import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE


def main():
    m = ir.Module()
    func_ty = ir.FunctionType(ir.VoidType(), [])
    i32_ty = ir.IntType(32)
    func = ir.Function(m, func_ty, name="printer")

    voidptr_ty = ir.IntType(8).as_pointer()

    fmt = "%s\n\0"
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                        bytearray(fmt.encode("utf8")))
    global_fmt = ir.GlobalVariable(m, c_fmt.type, name="fstr")
    global_fmt.linkage = 'internal'
    global_fmt.global_constant = True
    global_fmt.initializer = c_fmt

    fmt_i = "%i\n\0"
    c_fmt_i = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt_i)),
                        bytearray(fmt_i.encode("utf8")))
    global_fmt_i = ir.GlobalVariable(m, c_fmt_i.type, name="fstr_i")
    global_fmt_i.linkage = 'internal'
    global_fmt_i.global_constant = True
    global_fmt_i.initializer = c_fmt_i

    
    printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
    printf = ir.Function(m, printf_ty, name="printf")
    exit_ty = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
    exit_func = ir.Function(m, exit_ty, name="exit")

    builder = ir.IRBuilder(func.append_basic_block('entry'))
    fmt_arg = builder.bitcast(global_fmt, voidptr_ty)
    fmt_i_arg = builder.bitcast(global_fmt_i, voidptr_ty)
    ###### function body ########
    test = builder.sadd_with_overflow(i32_ty(2147483647), i32_ty(1), name = 'test')
    res = builder.extract_value(test, 0)
    bits = builder.extract_value(test, 1)
    with builder.if_then(bits):
        arg = "error: overflow!\0"
        c_str_val = ir.Constant(ir.ArrayType(ir.IntType(8), len(arg)),
                                bytearray(arg.encode("utf8")))
        c_str = builder.alloca(c_str_val.type)
        # fmt_arg = builder.bitcast(global_fmt, voidptr_ty)
        builder.store(c_str_val, c_str)
        builder.call(printf, [fmt_arg, c_str])
        builder.call(exit_func, [i32_ty(0)])
    
    
    builder.call(printf, [fmt_i_arg, res])

    

    # builder.call(exit_func, [i32_ty(5)])
    # arg = "error: overflow!\0"
    # c_str_val = ir.Constant(ir.ArrayType(ir.IntType(8), len(arg)),
    #                         bytearray(arg.encode("utf8")))
    # c_str = builder.alloca(c_str_val.type)
    # builder.store(c_str_val, c_str)
    # this val can come from anywhere
    # int_val = builder.add(i32_ty(5), i32_ty(2))
    # fmt_arg = builder.bitcast(global_fmt, voidptr_ty)
    # builder.call(printf, [fmt_arg, c_str, int_val])
    # builder.call(printf, [fmt_arg, c_str])



    builder.ret_void()

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    print(str(m))
    llvm_module = llvm.parse_assembly(str(m))
    tm = llvm.Target.from_default_triple().create_target_machine()

    with llvm.create_mcjit_compiler(llvm_module, tm) as ee:
        ee.finalize_object()
        fptr = ee.get_function_address("printer")
        py_func = CFUNCTYPE(None)(fptr)
        py_func()

if __name__ == "__main__":
    main()