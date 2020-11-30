# cmpl_proj1

## Authors: Yangjun Bie, Qieer Zhang

## Run the compiler:
```
python ekcc.py [-h|-?] [-v] [-O] [-emit-ast|-emit-llvm] -sysarg <arg1 arg2 arg3 ... > -o <output_file> <input_file>
```
sample command line to run the compiler:
```
python ekcc.py -O -jit -emit-ast -emit-llvm -sysarg 1 2 3 -o output.yaml test/correct.ek
```

For this part, we implement cint check: when overflow occurs, it will print 'error: overflow!' to the terminal and the call 'exit' to exit the program. 

To print 'error: overflow!' to the terminal, we correctly link to 'printf' function. But unfortunately, there are still something wrong with our print_statement, print_statements still get some errors. So we provided some .ek example which are quite simple and doesn't contain print_statement to show we implement this part. 