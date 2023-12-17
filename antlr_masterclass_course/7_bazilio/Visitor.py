import os
import operator

from typing import Any, Callable
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

    BOOLEAN_OP = [operator.eq, operator.ne, operator.lt, operator.le, operator.gt, operator.ge]

    def __init__(self, entry_proc='Main', entry_params=None):

        if entry_params is None:
            entry_params = []

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

    def visitRoot(self, ctx: BazilioParser.RootContext):
        for procDef in ctx.getChildren():
            self.visit(procDef)

        self._generate_music()

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
        """
        Grammar rule:
            input: INPUT VAR;
        """
        method_vars = self.stack[-1]
        var_name = ctx.VAR().getText()
        self._get_asserted_var(var_name, method_vars)
        temp = input("<?> x")
        method_vars[var_name] = float(temp) if "." in temp else int(temp)

    def visitOutput(self, ctx: BazilioParser.OutputContext):
        # output: OUTPUT expr+;
        children = list(ctx.getChildren())
        for expr in children[1:]:
            result = self.visit(expr)
            to_print = (self._str_list(result)
                        if isinstance(result, list)
                        else result)
            if expr != children[-1]:
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
            children = ['if', 'expr', 'LB', 'inss', 'RB', 'elif', 'expr', 'LB', 'inss', 'RB', 'elif', 'expr', 'LB', 'inss',
             'RB', 'elif', 'expr', 'LB', 'inss', 'RB', 'else', 'LB', 'inss', 'RB']
            >>> for i in range(0, len(children), 5):
            ...     condition = children[i:i+5]
            ...     print(condition)
            ['if', 'expr', 'LB', 'inss', 'RB']
            ['elif', 'expr', 'LB', 'inss', 'RB']
            ['elif', 'expr', 'LB', 'inss', 'RB']
            ['elif', 'expr', 'LB', 'inss', 'RB']
            ['else', 'LB', 'inss', 'RB']
        """
        children = list(ctx.getChildren())
        for i in range(0, len(children), 5):
            condition = children[i:i + 5]
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
        """
        children = list(ctx.getChildren())
        while 1 == self.visit(children[1]):
            self.visit(children[3])

    def visitReproduction(self, ctx: BazilioParser.ReproductionContext):
        """
        Grammar rule:
            reproduction: REPROD expr;
            REPROD: '(:)';
        """
        result = self.visit(ctx.getChild(1))
        notes = []
        if isinstance(result, list):
            for note_pre in result:
                note_pre = note_pre[:1] + "'" + note_pre[1:]
                notes.append(note_pre)
            self.score.extend(notes)

    def visitParamsId(self, ctx: BazilioParser.ParamsIdContext):
        """
        Grammar rule:
            paramsId: VAR*;
        """
        params_id = [param.getText() for param in list(ctx.getChildren())]
        return params_id

    def visitParamsExpr(self, ctx: BazilioParser.ParamsExprContext):
        """
        Grammar rule:
            paramsExpr: expr*;
        """
        params_expr = [self.visit(expr) for expr in list(ctx.getChildren())]
        return params_expr

    def visitProc(self, ctx: BazilioParser.ProcContext):
        """
        Grammar rule:
            proc: PROCEDURE paramsExpr;
            PROCEDURE: [A-Z][a-z0-9]*;
        """
        children = list(ctx.getChildren())
        name = children[0].getText()
        params_expr = self.visit(children[1])

        self.exec_proc(name, params_expr)

    def visitProcDef(self, ctx: BazilioParser.ProcDefContext):
        """
        Grammar rule:
            procDef: PROCEDURE paramsId LB instructions RB;
            PROCEDURE: [A-Z][a-z0-9]*;
        """
        name = ctx.PROCEDURE().getText()
        if name in self.procs:
            raise BazilioException(f"Procedure {name} already defined.")

        params = self.visit(ctx.paramsId())
        self.procs[name] = Process(name, params, ctx.instructions())

    def visitString(self, ctx: BazilioParser.StringContext):
        """
        Grammar rule:
            STRING: '"' ( '\\' . | ~('\\'|'"'))* '"';
        :param ctx: String text, for e.g.: "Hello my friend!"
        :return: Hello my friend!
        """
        string_value = ctx.getChild(0).getText()
        return string_value[1:-1]

    def visitPow(self, ctx: BazilioParser.MulContext):
        """
        Grammar rule:
            expr POW expr # Pow
        """
        return self._do_operation(ctx, operator.pow)

    def visitMul(self, ctx: BazilioParser.MulContext):
        """
        Grammar rule:
            expr MUL expr # Mul
        """
        return self._do_operation(ctx, operator.mul)

    def visitDiv(self, ctx: BazilioParser.DivContext):
        """
        Grammar rule:
            expr DIV expr # Div
        """
        children = list(ctx.getChildren())
        denominator = self.visit(children[2])
        if 0 == denominator:
            raise BazilioException("Division by zero.")
        return self.visit(children[0] / denominator)

    def visitMod(self, ctx: BazilioParser.ModContext):
        """
        Grammar rule:
            expr MOD expr # Mod
        """
        return self._do_operation(ctx, operator.mod)

    def visitAdd(self, ctx: BazilioParser.AddContext):
        """
        Grammar rule:
            expr ADD expr # Add
        """
        return self._do_operation(ctx, operator.add)

    def visitSub(self, ctx: BazilioParser.SubContext):
        """
        Grammar rule:
            expr SUB expr # Sub
        """
        return self._do_operation(ctx, operator.sub)

    def visitEq(self, ctx:BazilioParser.EqContext):
        """
        Grammar rule:
            expr EQ expr  # Eq
        """
        return self._do_operation(ctx, operator.eq)

    def visitGt(self, ctx: BazilioParser.GtContext):
        """
        Grammar rule:
            expr GT expr  # Gt
        """
        return self._do_operation(ctx, operator.gt)

    def visitLt(self, ctx: BazilioParser.LtContext):
        """
        Grammar rule:
            expr LT expr  # Lt
        """
        return self._do_operation(ctx, operator.lt)

    def visitGte(self, ctx: BazilioParser.GteContext):
        """
        Grammar rule:
            expr GTE expr # Gte
        """
        return self._do_operation(ctx, operator.ge)

    def visitLte(self, ctx: BazilioParser.LteContext):
        """
        Grammar rule:
            expr LTE expr # Lte
        """
        return self._do_operation(ctx, operator.le)

    def visitDif(self, ctx: BazilioParser.DifContext):
        """
        Grammar rule:
            expr DIF expr # Dif
        """
        return self._do_operation(ctx, operator.ne)

    def visitNum(self, ctx: BazilioParser.NumContext):
        """
        Grammar rule:
            NUM # Num
            NUM: [-]?[0-9]+('.'[0-9]+)?;
        """
        number = ctx.NUM().getText()
        return float(number) if "." in number else int(number)

    def visitVar(self, ctx: BazilioParser.VarContext):
        var_name = ctx.VAR().getText()
        method_vars = self.stack[-1]
        return self._get_asserted_var(var_name, method_vars)

    def visitInitList(self, ctx: BazilioParser.InitListContext):
        """
        Grammar rule:
            '{' expr* '}' # InitList
        """
        children = list(ctx.getChildren())
        values = [self.visit(child) for child in children[1:-1]]
        return values

    def visitSizeList(self, ctx: BazilioParser.SizeListContext):
        """
        Grammar rule:
            SIZELIST VAR  # SizeList
            SIZELIST: '#';
        """
        method_vars = self.stack[-1]
        var_name = ctx.VAR().getText()
        var_list = self._get_asserted_list(var_name, method_vars)
        size = len(var_list)
        return size

    def visitQuery(self, ctx: BazilioParser.QueryContext):
        """
        Grammar rule:
            query: VAR LK expr RK;
            LK: '[';
            RK: ']';
        :param ctx:
        :return:
        """
        var_name = ctx.VAR().getText()
        method_vars = self.stack[-1]
        var_list = self._get_asserted_list(var_name, method_vars)
        return var_list[self.visit(ctx.expr())]

    def visitAddingList(self, ctx: BazilioParser.AddingListContext):
        """
        Grammar rule:
            addingList: VAR ADDL expr;
            ADDL: '<<';
        :param ctx:
        :return:
        """
        var_name = ctx.VAR().getText()
        method_vars = self.stack[-1]
        var_list = self._get_asserted_list(var_name, method_vars)
        var_list.append(self.visit(ctx.expr()))

    def visitCutList(self, ctx: BazilioParser.CutListContext):
        """
        Grammar rule:
            cutList: CUTL VAR LK expr RK;
            CUTL: '|<';
            LK: '[';
            RK: ']';
        :param ctx:
        :return:
        """
        var_name = ctx.VAR().getText()
        method_vars = self.stack[-1]
        var_list = self._get_asserted_list(var_name, method_vars)
        index = self.visit(ctx.expr())
        self._assert_index_list(index, var_list)
        var_list.pop(index-1)

    def visitNote(self, ctx: BazilioParser.NoteContext):
        """
        Grammar rule:
            NOTE: [A-G][0-9]*;
        :param ctx:
        :return:
        """
        note = ctx.NOTE().getText()
        if len(note) == 2:
            return note

        default_note = note + "4"
        return default_note

    def visitSubExpr(self, ctx: BazilioParser.SubExprContext):
        """
        Grammar rule:
            LP expr RP
            LP: '(';
            RP: ')';
        :param ctx:
        :return:
        """
        return self.visit(ctx.expr())

    def exec_proc(self, name: str, params_values: list):
        # Error handling
        if name not in self.procs:
            raise BazilioException(f'The procedure "{name}"was not defined.')

        if len(self.procs[name].params) != len(params_values):
            raise BazilioException(f'The procedure "{name}" was waiting '
                                   f'for {len(self.procs[name].params)} '
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

    def _get_asserted_list(self, var_name: str, method_vars: dict) -> list:
        var_result = self._get_asserted_var(var_name, method_vars)
        if not isinstance(var_result, list):
            raise BazilioException(f"The {var_name} is not a list.")
        return var_result

    def _get_safe_note_or_comp(self, val1: int, val2: int, op: Callable[[int, int], int]):
        if op in self.BOOLEAN_OP:
            return int(op(val1, val2))

        safe_hash_value = op(val1, val2) % len(self.notes)
        for note, value in self.notes.items():
            if safe_hash_value == value:
                return note
        raise BazilioException("Invalid note type!")

    def _do_operation(self,
                      ctx: BazilioParser.ExprContext,
                      op: Callable[[int, int], int]):

        assert hasattr(ctx, 'expr'), f"expr must be present on ctx {ctx} to execute mathematical operation!"

        children = list(ctx.getChildren())

        left = children[0]
        right = children[2]

        is_left_note = left.getText() in self.notes.keys()
        is_right_note = right.getText() in self.notes.keys()
        is_left_var_note = self.stack[-1][left.getText()] in self.notes
        is_right_var_note = self.stack[-1][right.getText()] in self.notes

        if is_left_var_note:
            left = self.stack[-1][left.getText()]

        if is_right_var_note:
            right = self.stack[-1][right.getText()]

        # (pure|variable) note OP (pure|variable) note
        if is_left_note and is_right_note:
            val1 = self.notes[left.getText()]
            val2 = self.notes[right.getText()]
            return self._get_safe_note_or_comp(val1, val2, op)
        # (pure|variable) note OP integer
        elif is_left_note:
            val1 = self.notes[left.getText()]
            val2 = self.visit(ctx.expr(1))
            return self._get_safe_note_or_comp(val1, val2, op)
        # integer OP (pure|variable) note
        elif is_right_note:
            val1 = self.visit(ctx.expr(0))
            val2 = self.notes[right.getText()]
            return self._get_safe_note_or_comp(val1, val2, op)

        # integer OP integer
        val1 = self.visit(children[0])
        val2 = self.visit(children[2])

        return (op(val1, val2)
                if op in self.BOOLEAN_OP
                else int(op(val1, val2)))

    def _generate_music(self):
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        notes = self._notes_to_lilypond_fmt()

        with open(absolute_path + "./music.lily", "w") as f:
            f.write('\\version "2.20.0"' + os.linesep)
            f.write('\\score {' + os.linesep)
            f.write('\t\\absolute {' + os.linesep)
            f.write('\t\t\\tempo 4 = 120' + os.linesep)
            f.write(f'\t\t {notes}' + os.linesep)
            f.write('\t}' + os.linesep)
            f.write('\t\\layout { }' + os.linesep)
            f.write('\t\\midi { }' + os.linesep)
            f.write('}')

        os.system("lilypond music.lily")
        os.system("timidity -Ow -o music.wav music.midi")
        os.system("ffmpeg -i music.wav -codec:a libmp3lame -qscale:a 2 music.mp3")

    def _notes_to_lilypond_fmt(self) -> list:
        notes_music_upper = ' '.join(map(str, self.score))
        notes = notes_music_upper.lower()
        notes = [note[:1] + "'" + note[1:] for note in notes]
        return notes

    @classmethod
    def _str_list(cls, result) -> str:
        return (str(result)
                .replace(",", "")
                .replace("'", "")
                .replace("[", "{")
                .replace("]", "}"))

    @classmethod
    def _assert_index_list(cls, index: int, var_list: list):
        """
        In the Bazilio language, the index starts in the 1, not zero,
        that's why we check if it's equal or below zero.
        :index int: the index to validate
        :var_list list: the list to compare the size
        """
        if index <= 0 or index > len(var_list):
            raise BazilioException(f"Invalid list index {index}.")

    @classmethod
    def _get_asserted_var(cls, var_name: str, method_vars: dict) -> Any:
        if var_name not in method_vars:
            raise BazilioException(f'The variable "{var_name}" doesn\'t exists.')
        return method_vars[var_name]
