import ply.lex as lex

reserved_words = (
    'while',
    'for',
    'if',
    'else',
    'echo'
)

tokens = (
             'NUMBER',
             'ADD_OP',
             'SUB_OP',
             'MUL_OP',
             'DIV_OP',
             'INCREMENT',
             'DECREMENT',
             'ASSIGN',
             'ASSIGN_ADD',
             'ASSIGN_SUB',
             'ASSIGN_MUL',
             'ASSIGN_DIV',
             'COMP_EQUALS',
             'COMP_NOT_EQUALS',
             'COMP_GT',
             'COMP_GT_EQUALS',
             'COMP_LT',
             'COMP_LT_EQUALS',
             'STRING',
             'VARIABLE',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '();.{}"'


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_INCREMENT(t):
    r'\+\+'
    return t


def t_DECREMENT(t):
    r'--'
    return t


def t_ASSIGN_ADD(t):
    r'\+='
    return t


def t_ASSIGN_SUB(t):
    r'-='
    return t


def t_ASSIGN_MUL(t):
    r'\*='
    return t


def t_ASSIGN_DIV(t):
    r'/='
    return t


def t_COMP_EQUALS(t):
    r'=='
    return t


def t_COMP_NOT_EQUALS(t):
    r'!='
    return t


def t_COMP_LT_EQUALS(t):
    r'<='
    return t


def t_COMP_GT_EQUALS(t):
    r'>='
    return t


def t_ADD_OP(t):
    r'\+'
    return t


def t_SUB_OP(t):
    r'-'
    return t


def t_MUL_OP(t):
    r'\*'
    return t


def t_DIV_OP(t):
    r'/'
    return t


def t_ASSIGN(t):
    r'='
    return t


def t_COMP_GT(t):
    r'>'
    return t


def t_COMP_LT(t):
    r'<'
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
        return t
    raise NameError("Error: unknown token \"%s\" at line %s" % (t.value, t.lineno))

def t_STRING(t):
    r'\"([^\"]*?[^\"]*?)\"'
    t.value = str(t.value)
    t.value = t.value[1:-1]
    return t


def t_VARIABLE(t):
    r'\$\w[\w\d]*'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    raise SyntaxError("Illegal character '%s' at line %d" % (repr(t.value[0]), t.lineno))


lex.lex()

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok:
            break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))

