import operator

if __name__ and "." in __name__:
    from .BazilioParser import BazilioParser
    from .BazilioVisitor import BazilioVisitor
else:
    from BazilioParser import BazilioParser
    from BazilioVisitor import BazilioVisitor
from collections import defaultdict


class BazilioException(Exception):

    def __init__(self, message):
        self.message = f'Error: {message}'


class Process:

    def __init__(self, name, params, instructions):
        self.name = name
        self.params = params
        self.instructions = instructions


class Visitor(BazilioVisitor):

    def __init__(self, entry_proc='Main', entry_params=[]):
        self.entry_proc = entry_proc
        self.entry_param = entry_params
        self.procs = dict()
        self.stack = []
        # Fundamental list of the music score
        self.score = []
        self.notes = {
            "A0": 0, "B0": 1, "C1": 2, "D1": 3, "E1": 4, "F1": 5, "G1": 6,
            "A1": 7, "B1": 8, "C2": 9, "D2": 10, "E2": 11, "F2": 12, "G2": 13,
            "A2": 14, "B2": 15, "C3": 16, "D3": 17, "E3": 18, "F3": 19, "G3": 20,
            "A3": 21, "B3": 22, "C4": 23, "D4": 24, "E4": 25, "F4": 26, "G4": 27,
            "A4": 28, "B4": 29, "C5": 30, "D5": 31, "E5": 32, "F5": 33, "G5": 34,
            "A5": 35, "B5": 36, "C6": 37, "D6": 38, "E6": 39, "F6": 40, "G6": 41,
            "A6": 42, "B6": 43, "C7": 44, "D7": 45, "E7": 46, "F7": 47, "G7": 48,
            "A7": 49, "B7": 50, "C8": 51
        }

    def exec_proc(self, name: str, params_values: list):
        # Error handling
        if name not in self.procs:
            raise BazilioException(f'The proc "{name}" doesn\'t exists.')

        if len(self.procs[name].params) != len(params_values):
            raise BazilioException(f'The proc "{name}" was waiting for {len(self.procs[name].params)} '
                                   f'param(s), but {len(params_values)} was given.')

        new_vars = defaultdict(lambda: 0)
        for param, value in zip(self.procs[name].params, params_values):
            new_vars[param] = value

        # We push the arguments needed in procedure
        self.stack.append(new_vars)
        # We execute the procedure
        self.visit(self.procs[name].instructions)
        # We remove from the stack the executed procedure
        self.stack.pop()

    def visitRoot(self, ctx: BazilioParser.RootContext):
        for procdef in ctx.getChildren():
            self.visit(procdef)

    def visitInstructions(self, ctx: BazilioParser.InstructionsContext):
        for instruction in ctx.getChildren():
            self.visit(instruction)

    def visitInstruction(self, ctx: BazilioParser.InstructionContext):
        return self.visitChildren(ctx)

    def visitAssignment(self, ctx: BazilioParser.AssignmentContext):
        # assignment: VAR ASSIGN expr;
        method_vars = self.stack[-1]
        variable = ctx.VAR().getText()
        method_vars[variable] = self.visit(ctx.getChild(2))

    def visitInput(self, ctx: BazilioParser.InputContext):
        # input: INPUT VAR;
        method_vars = self.stack[-1]
        variable = ctx.VAR().getText()
        if variable not in method_vars:
            raise BazilioException(f'The variable "{variable}" doesn\'t exists.')

        temp = input("<?> x")
        method_vars[variable] = float(temp) if "." in temp else int(temp)

    def visitOutput(self, ctx: BazilioParser.OutputContext):
        # output: OUTPUT expr+;
        chd = list(ctx.getChildren())
        for expr in chd[1:]:
            result = self.visit(expr),
            # TODO Verificar se vai dar certo
            to_print = (self._str_list(result)
                        if isinstance(result, list)
                        else result)
            if expr != chd[-1]:
                print(to_print, end=" ")
            else:
                print(to_print)

    def visitConditional(self, ctx: BazilioParser.ConditionalContext):
        """
        Grammar rule:
            conditional: 'if' expr LB instructions RB
                ('elif' expr LB instructions RB)*
                ('else' LB instructions RB)?;
        It parses the conditional tree, for example:
            chd = ['if', 'expr', 'LB', 'inss', 'RB', 'elif', 'expr', 'LB', 'inss', 'RB', 'elif', 'expr', 'LB', 'inss',
             'RB', 'elif', 'expr', 'LB', 'inss', 'RB', 'else', 'LB', 'inss', 'RB']
            >>> for i in range(0, len(chd), 5):
            ...     condition = chd[i:i+5]
            ...     print(condition)
            ['if', 'expr', 'LB', 'inss', 'RB']
            ['elif', 'expr', 'LB', 'inss', 'RB']
            ['elif', 'expr', 'LB', 'inss', 'RB']
            ['elif', 'expr', 'LB', 'inss', 'RB']
            ['else', 'LB', 'inss', 'RB']

        :param ctx:
        :return:
        """
        chd = list(ctx.getChildren())
        for i in range(0, len(chd), 5):
            condition = chd[i:i + 5]
            if (("if" == condition[0].getText()
                 or "elif" == condition[0].getText())
                and 1 == self.visit(condition[1])):
                return self.visit(condition[3])
            elif "else" == condition[0].getText():
                return self.visit(condition[2])
            else:
                # TODO Verificar se terá problemas
                raise BazilioException("Invalid condition type")

    def visitWhile(self, ctx: BazilioParser.WhileContext):
        """
        Grammar rule:
            while: 'while' expr LB instructions RB;
        :param ctx:
        :return:
        """
        chd = list(ctx.getChildren())
        while 1 == self.visit(chd[1]):
            self.visit(chd[3])

    def visitReproduction(self, ctx: BazilioParser.ReproductionContext):
        pass

    def _str_list(self, result) -> str:
        return (str(result)
                .replace(",", "")
                .replace("'", "")
                .replace("[", "{")
                .replace("]", "}"))
