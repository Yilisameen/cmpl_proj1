import parser
import ply.yacc as yacc
import sys

flags = ['-h', '-?', '-v', '-O', '-emit-ast', '-emit-llvm', '-o']

args = sys.argv[1:]
input_file_name = ''
output_file_name = ''

for i in range(len(args)):
    arg = args[i]

    if i == len(args) - 1:
        if arg in flags or args[i - 1] == '-o':
            print('error: input file has not been specified.')
            sys.exit(4)
        else:
            input_file_name = arg
            break

    if args[i - 1] == '-o':
        continue

    if arg not in flags:
        print('error: flag ' + arg + ' is not a valid flag.')
        sys.exit(1)

    if (arg == '-emit-ast' and '-emit-llvm' in sys.argv) or (arg == '-emit-llvm' and '-emit-ast' in sys.argv):
        print('error: -emit-llvm and -emit-ast cannot be used at the same time.')
        sys.exit(2)

    if arg == '-h' or arg == '-?':
        print('''
            -h or -? produce some help/usage message and the names of the authors. 
            -v puts the compiler is "verbose" mode where additional information may be produced to standard output (otherwise, for correct inputs, no additional output may be produced, except for lines beginning with the string "warning: ").
            -O enables optimizations.
            -emit-ast causes the output file to contain the serialized format for the AST
            -emit-llvm will cause the LLVM IR to be produced (unoptimized, unless -O is provided).
            -o <output-file> names the output file.
            <input-file> names in input source code.
            ''')
        print('Authors: Yangjun Bie, Qieer Zhang')
    elif arg == '-v':
        print('-v not implement yet.')
    elif arg == '-O':
        print('-O not implement yet.')
    elif arg == '-emit-llvm':
        print('-emit-llvm not implement yet.')
    elif arg == '-emit-ast':
        continue
    elif arg == '-o':
        if i == len(args) - 1 or args[i + 1] in flags:
            print('error: output file has not been specified.')
            sys.exit(3)
        output_file_name = args[i + 1]

try:
    with open(input_file_name, 'r') as file:
        data = file.read()
except IOError:
    print('error: input file does not exist.')
    sys.exit(5)

ast = yacc.parse(data, debug = False).yaml_format()
with open(output_file_name, 'w') as file:
    file.write('---\n')
    file.write(ast)
    file.write('...\n')

sys.exit(0)

