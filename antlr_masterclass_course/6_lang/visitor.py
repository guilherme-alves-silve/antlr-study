import sys

from antlr4 import *
from LangLexer import LangLexer
from LangParser import LangParser
from EvalVisitor import EvalVisitor

input_stream = FileStream(sys.argv[1])
lexer = LangLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = LangParser(token_stream)
tree = parser.root()

visitor = EvalVisitor()
visitor.visit(tree)
