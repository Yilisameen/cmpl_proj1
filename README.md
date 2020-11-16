# cmpl_proj1

## Authors: Yangjun Bie, Qieer Zhang

## Run the compiler:
```
python ekcc.py [-h|-?] [-v] [-O] [-emit-ast|-emit-llvm] -sysarg <arg1 arg2 arg3 ... > -o <output_file> <input_file>
```
sample command line to run the compiler:
```
python ekcc.py -emit-ast -emit-llvm -sysarg 1 2 3 -o output.yaml test/test1.ek
```