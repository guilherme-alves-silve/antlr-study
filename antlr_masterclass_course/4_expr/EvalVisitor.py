if "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor


class EvalVisitor(ExprVisitor):

    def visitRoot(self, ctx: ExprParser.RootContext):
        children = list(ctx.getChildren())
        for i in range(len(children) - 1):
            self.visit(children[i])

    def visitCondition(self, ctx: ExprParser.ConditionContext):
        children = list(ctx.getChildren())
        if self.visit(children[1]) == 1:  # 'if' expr action+
            self.visit(ctx.action(0))  # ctx.action(0) == children[2]
        elif len(children) > 3:  # ('else' action+)?
            self.visit(ctx.action(1))

    def visitGt(self, ctx: ExprParser.GtContext):
        # '>' == children[1]
        children = list(ctx.getChildren())
        return int(self.visit(children[0]) > self.visit(children[2]))

    def visitLt(self, ctx: ExprParser.LtContext):
        # '<' == children[1]
        children = list(ctx.getChildren())
        return int(self.visit(children[0]) < self.visit(children[2]))

    def visitPrint(self, ctx: ExprParser.PrintContext):
        # 'print' == children[0]
        children = list(ctx.getChildren())
        print(self.visit(children[1]))

    def visitNum(self, ctx: ExprParser.NumContext):
        children = list(ctx.getChildren())
        return int(children[0].getText())
