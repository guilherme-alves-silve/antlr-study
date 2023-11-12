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
        ch = list(ctx.getChildren())
        # 'iff' expr action
        if 'iff' == ch[0].getText() and self.visit(ch[1]) == 1:
            return self.visit(ctx.action(0))
        # 'iff' expr action ('otherwise' action)?
        elif len(ch) >= 5 and 'otherwise' == ch[4].getText():
            return self.visit(ctx.action(1))
        else:
            print("WARNING!")

    def visitValue(self, ctx: ExprParser.ValueContext):
        ch = list(ctx.getChildren())
        # NAME ':=' expr
        self.vars[ch[0].getText()] = self.visit(ch[2])

    def visitWrite(self, ctx: ExprParser.WriteContext):
        ch = list(ctx.getChildren())
        # 'write' (expr|NAME)
        print(self.visit(ch[1]))

    def visitNext(self, ctx: ExprParser.NextContext):
        ch = list(ctx.getChildren())
        # 'next' expr
        print(self.visit(ch[1]) + 1)

    def visitPow(self, ctx: ExprParser.PowContext):
        # <assoc=right> expr POW expr
        pass

    def visitMul(self, ctx:ExprParser.MulContext):
        # expr MUL expr
        pass

    def visitDiv(self, ctx:ExprParser.DivContext):
        # expr DIV expr
        pass

    def visitAdd(self, ctx: ExprParser.AddContext):
        # expr ADD expr
        pass

    def visitSub(self, ctx: ExprParser.SubContext):
        # expr SUB expr
        pass

    def visitEq(self, ctx: ExprParser.EqContext):
        # expr EQ  expr
        pass

    def visitDif(self, ctx: ExprParser.DifContext):
        # expr DIF expr
        pass

    def visitGt(self, ctx: ExprParser.GtContext):
        # expr GT expr
        pass

    def visitLt(self, ctx: ExprParser.LtContext):
        # expr LT expr
        pass

    def visitNum(self, ctx: ExprParser.NumContext):
        return int(ctx.NUM())
