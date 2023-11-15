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
        elif len(ch) >= 5 and 'otherwise' == ch[3].getText():
            return self.visit(ctx.action(1))

    def visitValue(self, ctx: ExprParser.ValueContext):
        ch = list(ctx.getChildren())
        # NAME ':=' expr
        self.vars[ch[0].getText()] = self.visit(ch[2])

    def visitWrite(self, ctx: ExprParser.WriteContext):
        ch = list(ctx.getChildren())
        # 'write' expr
        print(self.visit(ch[1]))

    def visitNext(self, ctx: ExprParser.NextContext):
        ch = list(ctx.getChildren())
        # 'next' (expr|NAME)
        if ctx.NAME():
            self.vars[ctx.NAME()] += 1
            print(self.vars[ctx.NAME()])
        else:
            print(self.visit(ch[1]) + 1)

    def visitPow(self, ctx: ExprParser.PowContext):
        ch = list(ctx.getChildren())
        # <assoc=right> expr POW expr
        return self.visit(ch[0])**self.visit(ch[2])

    def visitMul(self, ctx: ExprParser.MulContext):
        ch = list(ctx.getChildren())
        # expr MUL expr
        return self.visit(ch[0]) * self.visit(ch[2])

    def visitDiv(self, ctx: ExprParser.DivContext):
        ch = list(ctx.getChildren())
        # expr DIV expr
        return self.visit(ch[0]) / self.visit(ch[2])

    def visitAdd(self, ctx: ExprParser.AddContext):
        ch = list(ctx.getChildren())
        # expr ADD expr
        return self.visit(ch[0]) + self.visit(ch[2])

    def visitSub(self, ctx: ExprParser.SubContext):
        ch = list(ctx.getChildren())
        # expr SUB expr
        return self.visit(ch[0]) - self.visit(ch[2])

    def visitEq(self, ctx: ExprParser.EqContext):
        ch = list(ctx.getChildren())
        # expr EQ  expr
        return int(self.visit(ch[0]) == self.visit(ch[2]))

    def visitDif(self, ctx: ExprParser.DifContext):
        ch = list(ctx.getChildren())
        # expr DIF expr
        return int(self.visit(ch[0]) != self.visit(ch[2]))

    def visitGt(self, ctx: ExprParser.GtContext):
        ch = list(ctx.getChildren())
        # expr GT expr
        return int(self.visit(ch[0]) > self.visit(ch[2]))

    def visitLt(self, ctx: ExprParser.LtContext):
        ch = list(ctx.getChildren())
        # expr LT expr
        return int(self.visit(ch[0]) < self.visit(ch[2]))

    def visitNum(self, ctx: ExprParser.NumContext):
        return int(ctx.getChild(0).getText())

    def visitName(self, ctx: ExprParser.NameContext):
        variable = self.vars[ctx.NAME().getText()]
        if not variable:
            raise SystemError(f"Variable {ctx.NAME().getText()} doesn't exists!")

        return int(variable)
