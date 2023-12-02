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
        self.procs = []
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
        for ch in ctx.getChildren():
            self.visit(ch)



