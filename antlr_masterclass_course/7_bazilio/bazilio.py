import sys

from antlr4 import *
from BazilioLexer import BazilioLexer
from BazilioParser import BazilioParser
from EvalVisitor import EvalVisitor

input_stream = FileStream(sys.argv[1], encoding="utf-8")
lexer = BazilioLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = BazilioParser(token_stream)
tree = parser.root()

if len(sys.argv) > 2:
    # example: python3 bazilio.py music.bzl Hanoi
    eval_visitor = EvalVisitor(sys.argv[2])
else:
    eval_visitor = EvalVisitor()

eval_visitor.visit(tree)
