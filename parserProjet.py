import ply.yacc as yacc
from lexProjet import tokens
import AST

vars = {}

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'SUB_OP'),
    ('left', 'MUL_OP'),
    ('left', 'DIV_OP')
)

# ---------------
# Programme
# ---------------
def p_programme(p):
    ''' programme : statement
                | statement programme '''
    try:
        p[0] = AST.ProgramNode([p[1]] + p[2].children)
    except:
        p[0] = AST.ProgramNode(p[1])


# ---------------
# Statement
# ---------------
def p_statement(p):
    ''' statement : assignation
                | incrementexpression
                | structure '''
    p[0] = p[1]


def p_statement_echo(p):
    ''' statement : ECHO echoexpression '''
    p[0] = AST.EchoNode(p[2])


def p_echoexpression(p):
    ''' echoexpression : expression
                        | expression '.' echoexpression '''
    try:
        p[0] = AST.EchoExpressionNode([p[1], p[3]])
    except:
        p[0] = AST.EchoExpressionNode(p[1])


# ---------------
# Structure
# ---------------
def p_structure_while(p):
    ''' structure : WHILE '(' comparaison ')' '{' programme '}' '''
    p[0] = AST.WhileNode([p[3], p[6]])


def p_structure_if(p):
    ''' structure : IF '(' comparaison ')' '{' programme '}' '''
    p[0] = AST.IfNode(p[3], [p[6]])


def p_structure_if_else(p):
    ''' structure : IF '(' comparaison ')' '{' programme '}' ELSE '{' programme '}' '''
    p[0] = AST.IfNode(p[3], [p[6], p[10]])


def p_structure_for(p):
    ''' structure : FOR '(' assignation ';' comparaison ';' assignation ')' '{' programme '}'
                | FOR '(' assignation ';' comparaison ';' incrementexpression ')' '{' programme '}' '''
    p[0] = AST.ForNode(p[3], p[5], p[7], p[10])


# ---------------
# Assignation
# ---------------
def p_assignation(p):
    ''' assignation : VARIABLE ASSIGN expression '''
    p[0] = AST.AssignNode([AST.VariableNode(p[1]), p[3]])


def p_assignation_operation(p):
    ''' assignation : VARIABLE ASSIGN_ADD expression
                    | VARIABLE ASSIGN_SUB expression
                    | VARIABLE ASSIGN_MUL expression
                    | VARIABLE ASSIGN_DIV expression '''

    p[0] = AST.AssignOpNode(p[2], [AST.VariableNode(p[1]), p[3]])


# ---------------
# Comparaison
# ---------------
def p_comparaison(p):
    ''' comparaison : expression COMP_LT expression
                    | expression COMP_GT expression
                    | expression COMP_LT_EQUALS expression
                    | expression COMP_GT_EQUALS expression
                    | expression COMP_EQUALS expression
                    | expression COMP_NOT_EQUALS expression '''
    p[0] = AST.CompareNode(p[2], [p[1], p[3]])


# ---------------
# Expression
# ---------------
def p_expression(p):
    ''' expression : NUMBER
                | STRING '''
    p[0] = AST.ExpressionNode(p[1])


def p_expression_variable(p):
    ''' expression : VARIABLE '''
    p[0] = AST.VariableNode(p[1])


def p_expression_op(p):
    '''expression : expression ADD_OP expression
               | expression MUL_OP expression
               | expression SUB_OP expression
               | expression DIV_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_expression_increment(p):
    ''' incrementexpression : VARIABLE INCREMENT
                    | VARIABLE DECREMENT '''
    p[0] = AST.IncrementNode(p[2], AST.VariableNode(p[1]))


def p_error(p):
    if p:
        raise SyntaxError("Syntax error in line %d (token = \"%s\")" % (p.lineno, p.value))
    else:
        raise SyntaxError("Sytax error: unexpected end of file!")


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print(result)

        graph = result.makegraphicaltree()
    else:
        print("Parsing returned no result!")
