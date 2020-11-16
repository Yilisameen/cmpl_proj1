from llvmlite import ir

class ExternalFunctions:
	def __init__(self, module, sys_args):
		self.module = module
		self.sys_args = [1, 2, 3]
		self.get_printf()

	def get_arg(self, func_map):
		sys_args = [int(float(value)) for value in self.sys_args]

		array_type = ir.ArrayType(ir.IntType(32), len(sys_args))
		arr = ir.Constant(array_type, sys_args)

		fnty = ir.FunctionType(ir.IntType(32), [ir.IntType(32)])
		func = ir.Function(self.module, fnty, name="getarg")
		func_map["getarg"] = func

		blk = func.append_basic_block("entry")
		builder = ir.IRBuilder(blk)

		ptr = builder.alloca(array_type)

		index = func.args[0]
		ptr_arg = builder.alloca(ir.IntType(32))
		builder.store(index, ptr_arg)
		value = builder.load(ptr_arg)

		for number, arg in enumerate(sys_args):
			int_1 = ir.Constant(ir.IntType(32), arg)
			builder.insert_value(arr, int_1, number)
			builder.store(arr, ptr)

		int_0 = ir.Constant(ir.IntType(32), 0)
		address = builder.gep(ptr, [int_0, value])
		builder.ret(builder.load(address))

	def get_argf(self, func_map):
		sys_args = [float(value) for value in self.sys_args]

		array_type = ir.ArrayType(ir.FloatType(), len(sys_args))
		arr = ir.Constant(array_type, sys_args)

		fnty = ir.FunctionType(ir.FloatType(), [ir.IntType(32)])
		func = ir.Function(self.module, fnty, name="getargf")
		func_map["getargf"] = func

		blk = func.append_basic_block("entry")
		builder = ir.IRBuilder(blk)

		ptr = builder.alloca(array_type)

		index = func.args[0]
		ptr_arg = builder.alloca(ir.IntType(32))
		builder.store(index, ptr_arg)
		value = builder.load(ptr_arg)

		for number, arg in enumerate(sys_args):
			float_1 = ir.Constant(ir.FloatType(), arg)
			builder.insert_value(arr, float_1, number)
			builder.store(arr, ptr)

		int_0 = ir.Constant(ir.IntType(32), 0)
		address = builder.gep(ptr, [int_0, value])
		builder.ret(builder.load(address))

	def get_printf(self):
		char_pointer = ir.IntType(8).as_pointer()
		fnty1 = ir.FunctionType(ir.VoidType(), [char_pointer])
		self.print_string = ir.Function(self.module, fnty1, name="printString")

		fnty2 = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
		self.print_int = ir.Function(self.module, fnty2, name="printInt")

		fnty3 = ir.FunctionType(ir.VoidType(), [ir.FloatType()])
		self.print_float = ir.Function(self.module, fnty3, name="printFloat")







