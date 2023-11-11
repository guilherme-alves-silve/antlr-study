if "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor


class EvalVisitor(ExprVisitor):

    def visitRoot(self, ctx: ExprParser.RootContext):
        children = list(ctx.getChildren())
        print(self.visit(children[0]))

    def visitNum(self, ctx: ExprParser.NumContext):
        children = list(ctx.getChildren())
        return int(children[0].getText())

    def visitMul(self, ctx: ExprParser.MulContext):
        children = list(ctx.getChildren())
        return self.visit(children[0]) * self.visit(children[2])

    def visitDiv(self, ctx: ExprParser.DivContext):
        children = list(ctx.getChildren())
        return self.visit(children[0]) / self.visit(children[2])

    def visitPlus(self, ctx: ExprParser.PlusContext):
        children = list(ctx.getChildren())
        return self.visit(children[0]) + self.visit(children[2])

    def visitSub(self, ctx: ExprParser.SubContext):
        children = list(ctx.getChildren())
        return self.visit(children[0]) - self.visit(children[2])
