import operator
if "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor


OPS = {
    '^': operator.pow,
    '*': operator.mul,
    '/': operator.truediv,
    '+': operator.add,
    '-': operator.sub
}


class EvalVisitor(ExprVisitor):

    def __init__(self):
        self.variables = dict()

    def visitRoot(self, ctx:ExprParser.RootContext):
        children = list(ctx.getChildren())
        # The last children is EOF
        for i in range(len(children) - 1):
            print(self.visit(children[i]))

    def visitExpr(self, ctx: ExprParser.ExprContext):
        children = list(ctx.getChildren())

        if len(children) == 1:  # NUM case
            return int(children[0].getText())
        elif len(children) == 3:
            op = children[1].getText()
            func = OPS[op]
            if func:
                return func(self.visit(children[0]), self.visit(children[2]))
            else:
                raise SyntaxError(f"Invalid operator {op}")

    def visitAction(self, ctx: ExprParser.ActionContext):
        children = list(ctx.getChildren())
        if len(children) == 3:
            action = children[1].getText()
            if ':=' == action:
                var_name = children[0].getText()
                self.variables[var_name] = self.visit(children[2])
                return f'assigment to {var_name}'
            else:
                raise SyntaxError(f"Invalid action {action}")
        elif len(children) == 2:
            action = children[0].getText()
            if 'write' == action:
                return self.variables[children[1].getText()]
        else:
            raise SyntaxError(f"Invalid action")
