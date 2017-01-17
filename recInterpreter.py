import AST
from AST import addToClass
from functools import reduce

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
    print('programnode')
    for c in self.children:
        c.execute()


@addToClass(AST.VariableNode)
def execute(self):
    print('variablenode')
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("*** Error: variable %s undefined!" % self.tok)
            return self.tok
    return self.tok


@addToClass(AST.OpNode)
def execute(self):
    print('opnode')
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST.AssignNode)
def execute(self):
    print('assignnode')
    try:
        vars[self.children[0].tok] = self.children[1].execute()
    except AttributeError:
        vars[self.children[0].tok] = self.children[1]


@addToClass(AST.CompareNode)
def execute(self):
    print('comparenode')
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(compare_operations[self.op], args)

@addToClass(AST.EchoNode)
def execute(self):
    print('echonode')
    print(self.children[0].execute())


@addToClass(AST.WhileNode)
def execute(self):
    print('whilenode')
    while self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.IfNode)
def execute(self):
    print('ifnode')
    if self.comparaison.execute():
        self.children[0].execute()


@addToClass(AST.ExpressionNode)
def execute(self):
    print("expression")
    return self.value

@addToClass(AST.AssignOpNode)
def execute(self):
    print("assignop")
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    temp = reduce(assign_operations[self.op], args)
    vars[self.children[0].tok] = temp

if __name__ == "__main__":
    from parserProjet import parse
    import sys

    print('MAIN')
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    ast.execute()
