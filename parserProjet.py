import ply.yacc as yacc

from lexProjet import tokens
import AST

vars = {}


def p_programme(p):
    ''' programme : statement
    | statement programme '''
    try:
        p[0] = AST.ProgramNode([p[1]] + p[2].children)
    except:
        p[0] = AST.ProgramNode(p[1])


def p_statement(p):
    ''' statement : assignation ';'
        | structure
        | ECHO expression_printable '''
    try:
        p[0] = AST.EchoNode(p[2])
    except:
        p[0] = p[1]


def p_structure_while(p):
    ''' structure : WHILE '(' expression ')' '{' programme '}' '''
    p[0] = AST.WhileNode([p[3], p[6]])


def p_structure_if(p):
    ''' structure : IF '(' expression ')' '{' programme '}' '''
    p[0] = AST.IfNode([p[3], p[6]])


def p_structure_if_else(p):
    ''' structure : IF '(' expression ')' '{' programme '}' ELSE '{' programme '}' '''
    p[0] = AST.IfNode([p[3], [p[6], p[10]]])

def p_structure_for(p):
    ''' structure : FOR '(' assignation ';' comparaison ';' assignation ')' '{' programme '}'
    |  FOR '(' assignation ';' comparaison ';' expression ')' '{' programme '}' '''
    p[0] = AST.ForNode(p[2],p[4],p[6],p[9]);

def p_assignation(p):
    ''' assignation : VARIABLE '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])

#def p_comparaison(p):TODO

def p_printable(p):
    ''' printable : STRING
        | printable '.' printable
        | printable '.' expression
        | expression '.' printable '''
    try:
        p[0] = AST.PrintableNode(p[2],p[4])
    except:
        p[0] = AST.PrintableNode(p[2])

#def p_expression(p):



def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_printable(p):
    ''' expression_printable : '"' IDENTIFIER '"'
        | expression_printable '.' expression_printable '''
    p[0] = AST.PrintableNode(p[2])


def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])


def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])




def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print(result)

        import os

        graph = result.makegraphicaltree()
    else:
        print("Parsing returned no result!")
