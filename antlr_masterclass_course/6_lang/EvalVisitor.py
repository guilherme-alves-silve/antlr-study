from antlr4.tree.Tree import ErrorNodeImpl

if __name__ and "." in __name__:
    from .LangParser import LangParser
    from .LangVisitor import LangVisitor
else:
    from LangParser import LangParser
    from LangVisitor import LangVisitor


class EvalVisitor(LangVisitor):

    def __init__(self):
        variables = dict()
        self.stack = [variables]

    def visitRoot(self, ctx: LangParser.RootContext):
        for ch in ctx.getChildren():
            self.visit(ch)

    def visitInstructions(self, ctx: LangParser.InstructionsContext):
        for ch in ctx.getChildren():
            self.visit(ch)

    def visitWhile(self, ctx: LangParser.WhileContext):
        ch = list(ctx.getChildren())
        # 'while' expr instruction+
        while 1 == self.visit(ch[1]):
            self.visit(ch[2])

    def visitOutput(self, ctx: LangParser.OutputContext):
        ch = list(ctx.getChildren())
        print(self.visit(ch[1]))

    def visitAssign(self, ctx: LangParser.AssignContext):
        if not ctx.ASSIGN():
            raise SyntaxError('Missing "<-" operator')
        self.stack[-1][ctx.VAR().getText()] = self.visit(ctx.getChild(2))

    def visitAdd(self, ctx: LangParser.AddContext):
        ch = list(ctx.getChildren())
        return self.visit(ch[0]) + self.visit(ch[2])

    def visitSub(self, ctx: LangParser.SubContext):
        ch = list(ctx.getChildren())
        return self.visit(ch[0]) - self.visit(ch[2])

    def visitGt(self, ctx: LangParser.GtContext):
        ch = list(ctx.getChildren())
        return int(self.visit(ch[0]) > self.visit(ch[2]))

    def visitLt(self, ctx: LangParser.LtContext):
        ch = list(ctx.getChildren())
        return int(self.visit(ch[0]) < self.visit(ch[2]))

    def visitEq(self, ctx: LangParser.EqContext):
        ch = list(ctx.getChildren())
        return int(self.visit(ch[0]) == self.visit(ch[2]))

    def visitVar(self, ctx: LangParser.VarContext):
        return self.stack[-1][ctx.VAR().getText()]

    def visitNum(self, ctx: LangParser.NumContext):
        return int(ctx.NUM().getText())
