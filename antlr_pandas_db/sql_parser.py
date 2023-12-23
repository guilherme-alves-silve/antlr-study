import os
import pandas as pd

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from tabulate import tabulate
from PocketsLexer import PocketsLexer
from PocketsParser import PocketsParser
from PocketsListener import PocketsListener


class SQLParser(PocketsListener):

    def __init__(self, base_path):
        self.tokens = None
        self.base_path = base_path

    def parse(self, sql: str):
        print(f"Parsing SQL: {sql}")
        data = InputStream(sql)
        lexer = PocketsLexer(data)
        stream = CommonTokenStream(lexer)
        self.tokens = stream
        parser = PocketsParser(stream)
        tree = parser.pocket()
        walker = ParseTreeWalker()
        walker.walk(self, tree)

    def exitCreate(self, ctx: PocketsParser.CreateContext):
        file_name = ctx.fileIdentifier().getText()
        column_names_list = ctx.columnNames().identifier()
        column_names = [column_name.getText() for column_name in column_names_list]
        df = pd.DataFrame(columns=column_names)
        print(f"Saving to {self.base_path}/{file_name}")
        full_file_name = os.path.join(self.base_path, file_name)
        df.to_csv(full_file_name, index=False)

    def exitInsert(self, ctx: PocketsParser.InsertContext):
        file_name = ctx.fileIdentifier().getText()
        full_file_name = os.path.join(self.base_path, file_name)
        df = self._get_valid_df(full_file_name)
        column_names_list = ctx.columnNames().identifier()
        rows_list = ctx.values()
        for row_values in rows_list:
            column_values = row_values.constants().constant()
            if len(column_names_list) != len(column_values):
                raise RuntimeError("column to Values mismatch")
            line = [column_value.getText() for column_value in column_values]
            df.loc[len(df.index)] = line

        df.to_csv(full_file_name, index=False)

    def exitSelect(self, ctx: PocketsParser.SelectContext):
        file_name = ctx.fileIdentifier().getText()
        full_file_name = os.path.join(self.base_path, file_name)
        df = self._get_valid_df(full_file_name)
        bool_exp = ctx.booleanExpression()
        if bool_exp:
            expression = self.tokens.getText(bool_exp.start, bool_exp.stop)
            df = df.query(expression)
        expression_list_ctx = ctx.expressionList()
        expression_list = expression_list_ctx.expression()
        if len(expression_list) == 1 and expression_list[0].getText() == '*':
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
        else:
            new_df = df[[exp.getText() for exp in expression_list]]
            print(tabulate(new_df, headers='keys', tablefmt='psql', showindex=False))

    def exitDelete(self, ctx: PocketsParser.DeleteContext):
        file_name = ctx.fileIdentifier().getText()
        full_file_name = os.path.join(self.base_path, file_name)
        if os.path.exists(full_file_name):
            os.remove(full_file_name)
        else:
            raise FileNotFoundError(str(full_file_name))

    @classmethod
    def _get_valid_df(cls, full_file_name: str) -> pd.DataFrame:
        if not os.path.exists(full_file_name):
            raise FileNotFoundError(str(full_file_name))
        return pd.read_csv(full_file_name)
