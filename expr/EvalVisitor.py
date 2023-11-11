if "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor


class EvalVisitor(ExprVisitor):

    def visitRoot(self, ctx:ExprParser.RootContext):
        children = list(ctx.getChildren())
        print(self.visit(children[0]))

    def visitExpr(self, ctx:ExprParser.ExprContext):
        children = list(ctx.getChildren())

        if len(children) == 1:
            return int(children[0].getText())
        elif len(children) == 3:
            op = children[1]
            if '+' == op.getText():
                return self.visit(children[0]) + self.visit(children[2])
            elif '-' == op.getText():
                return self.visit(children[0]) - self.visit(children[2])
            else:
                raise SyntaxError(f"Invalid operator {op.getText()}")
