import AST
import logging as log
from AST import addToClass
from functools import reduce

# log.basicConfig(level=log.DEBUG)

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

assign_operations = {
    '+=': lambda x, y: x + y,
    '-=': lambda x, y: x - y,
    '*=': lambda x, y: x * y,
    '/=': lambda x, y: x / y,
}

compare_operations = {
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
}
vars = {}


@addToClass(AST.ProgramNode)
def execute(self):
    log.debug('ProgramNode')
    for c in self.children:
        c.execute()


@addToClass(AST.VariableNode)
def execute(self):
    log.debug('VariableNode')
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("*** Error: variable %s undefined!" % self.tok)
            return self.tok
    return self.tok


@addToClass(AST.OpNode)
def execute(self):
    log.debug('OpNode')
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST.IncrementNode)
def execute(self):
    log.debug('IncrementNode')
    if self.op == '++':
        vars[self.children[0].tok] += 1
    else:
        vars[self.children[0].tok] -= 1


@addToClass(AST.AssignNode)
def execute(self):
    log.debug('AssignNode')
    try:
        vars[self.children[0].tok] = self.children[1].execute()
    except AttributeError:
        vars[self.children[0].tok] = self.children[1]


@addToClass(AST.CompareNode)
def execute(self):
    log.debug('CompareNode')
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(compare_operations[self.op], args)


@addToClass(AST.EchoNode)
def execute(self):
    log.debug('EchoNode')
    print(self.children[0].execute())

@addToClass(AST.EchoExpressionNode)
def execute(self):
    log.debug('EchoExpressionNode')
    string = ""
    for c in self.children:
        string += str(c.execute())
    return string

@addToClass(AST.WhileNode)
def execute(self):
    log.debug('WhileNode')
    while self.children[0].execute():
        self.children[1].execute()


@addToClass(AST.IfNode)
def execute(self):
    log.debug('IfNode')
    if self.comparaison.execute():
        self.children[0].execute()
    else:
        if self.nbargs == 2:
            self.children[1].execute()


@addToClass(AST.ExpressionNode)
def execute(self):
    log.debug('ExpressionNode')
    return self.value


@addToClass(AST.AssignOpNode)
def execute(self):
    log.debug('AssignOpNode')
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    temp = reduce(assign_operations[self.op], args)
    vars[self.children[0].tok] = temp


if __name__ == "__main__":
    from parserProjet import parse
    import sys

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
