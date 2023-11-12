import operator

if __name__ and '.' in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor


class EvalVisitor(ExprVisitor):

    def __init__(self):
        self.vars = dict()

    def visitRoot(self, ctx: ExprParser.RootContext):
        ch = list(ctx.getChildren())
        for i in range(len(ch) - 1):
            self.visit(ch[i])

    def visitCondition(self, ctx: ExprParser.ConditionContext):
        pass