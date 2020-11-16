from llvmlite import ir

# Create some useful types
double = ir.DoubleType()
fnty = ir.FunctionType(double, (double, double))

# Create an empty module...
module = ir.Module(name=__file__)
# and declare a function named "fpadd" inside it
func = ir.Function(module, fnty, name="fpadd")

# Now implement the function
block = func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)
a, b = func.args
result = builder.fadd(a, b, name = "res")
builder.ret(result)

tst_fnty = ir.FunctionType(double, [])
func_tst = ir.Function(module, tst_fnty, name = "tst")
block = func.append_basic_block(name="entry")

# func2 = ir.Function(module, fnty, name="fpsub")
# block = func2.append_basic_block(name="entry")
# builder = ir.IRBuilder(block)
# a, b = func2.args
# result1 = builder.call(func, [a, b])
# builder.ret(result1)

# a, b = func2.args
# result = builder.fsub(a,b, name = "res")
# builder.ret(result)

# Print the module IR
print(module)