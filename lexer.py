import ply.lex as lex

# List of token names.   This is always required
reserved = {
    'extern' : "EXTERN",
    'def' : 'DEF',
    'return' : 'RETURN',
    'while' : 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'print' : 'PRINT',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'int' : 'INT',
    'cint' : 'CINT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'void' : 'VOID',
    'ref' : 'REF',
    'noalias': 'NOALIAS'
}

tokens = [
        'EQUALITY', 'AND', 'OR',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
        'NOT', 'COMMA', 'SEMICOLON', 'EQUAL', 'LESS', 'GREATER', 'DOLLAR',
        'NUMBER', 'ID', 'SLIT', ] + list(reserved.values())

# Regular expression rules for simple tokens
t_EQUALITY = r'=='
t_AND = r'&&'
t_OR = r'\|\|'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_NOT = r'!'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUAL = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_DOLLAR = r'\$'
t_NUMBER = r'[0-9]+(\.[0-9]+)?'
t_SLIT = r'"[^"\n\r]*"'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
# Ignore comments
t_ignore_COMMENT = r'\#.*'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


data = '''
def void things (ref int $n) {
  while (!($n > 100)) {
    $n = $n * $n - 2;
  }
}

def int run () {
    print "fib(5):";
    int $val = fib(5);
    print $val;
    
    print "fib(5)+1:";
    inc($val);
    print $val;

    print "something else:";
    things($val);
    print $val;


    return 0;
}
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
