import re
from enum import Enum


# TOKEN TYPES


class TokenType(Enum):
    SCI_NUMBER = "SCI_NUMBER"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    FUNCTION = "FUNCTION"
    ASSIGN = "ASSIGN"
    IDENT = "IDENT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"



# LEXER


class Lexer:
    def __init__(self):
        self.token_specification = [
            ('SCI_NUMBER', r'\d+(\.\d+)?[eE][+-]?\d+'),
            ('FLOAT', r'\d+\.\d+'),
            ('INTEGER', r'\d+'),
            ('FUNCTION', r'sin|cos|tan'),
            ('ASSIGN', r'='),
            ('IDENT', r'[a-zA-Z_]\w*'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MUL', r'\*'),
            ('DIV', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('WS', r'\s+'),
            ('MISMATCH', r'.'),
        ]

        self.regex = '|'.join(
            f'(?P<{name}>{pattern})'
            for name, pattern in self.token_specification
        )

    def tokenize(self, code):
        tokens = []

        for match in re.finditer(self.regex, code):

            kind = match.lastgroup
            value = match.group()

            if kind == "WS":
                continue

            elif kind == "MISMATCH":
                raise SyntaxError(
                    f"Unexpected character {value}"
                )

            else:
                tokens.append({
                    "type": TokenType[kind],
                    "value": value
                })

        return tokens



# AST NODES


class ASTNode:
    pass


class NumberNode(ASTNode):

    def __init__(self, value):
        self.value = value


class VariableNode(ASTNode):

    def __init__(self, name):
        self.name = name


class BinaryOpNode(ASTNode):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class FunctionNode(ASTNode):

    def __init__(self, name, argument):
        self.name = name
        self.argument = argument



# PARSER


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0

    def current(self):

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None

    def eat(self, token_type):

        token = self.current()

        if token and token["type"] == token_type:
            self.pos += 1
            return token

        raise SyntaxError(f"Expected {token_type}")

    def parse(self):

        return self.expression()

    # expression -> term ((+|-) term)*

    def expression(self):

        node = self.term()

        while self.current() and self.current()["type"] in (
                TokenType.PLUS,
                TokenType.MINUS):

            operator = self.current()["value"]

            self.pos += 1

            right = self.term()

            node = BinaryOpNode(node, operator, right)

        return node

    # term -> factor ((*|/) factor)*

    def term(self):

        node = self.factor()

        while self.current() and self.current()["type"] in (
                TokenType.MUL,
                TokenType.DIV):

            operator = self.current()["value"]

            self.pos += 1

            right = self.factor()

            node = BinaryOpNode(node, operator, right)

        return node

    # factor -> number | variable | function | (expression)

    def factor(self):

        token = self.current()

        if token["type"] in (
                TokenType.INTEGER,
                TokenType.FLOAT,
                TokenType.SCI_NUMBER):

            self.pos += 1

            return NumberNode(token["value"])

        if token["type"] == TokenType.IDENT:

            self.pos += 1

            return VariableNode(token["value"])

        if token["type"] == TokenType.FUNCTION:

            func_name = token["value"]

            self.pos += 1

            self.eat(TokenType.LPAREN)

            argument = self.expression()

            self.eat(TokenType.RPAREN)

            return FunctionNode(func_name, argument)

        if token["type"] == TokenType.LPAREN:

            self.pos += 1

            node = self.expression()

            self.eat(TokenType.RPAREN)

            return node

        raise SyntaxError("Invalid Syntax")


# AST PRINT


def print_ast(node, indent=0):

    space = "  " * indent

    if isinstance(node, NumberNode):

        print(space + f"Number({node.value})")

    elif isinstance(node, VariableNode):

        print(space + f"Variable({node.name})")

    elif isinstance(node, BinaryOpNode):

        print(space + f"Operator({node.op})")

        print_ast(node.left, indent + 1)

        print_ast(node.right, indent + 1)

    elif isinstance(node, FunctionNode):

        print(space + f"Function({node.name})")

        print_ast(node.argument, indent + 1)



# MAIN


if __name__ == "__main__":

    lexer = Lexer()

    print("Parser & AST Builder")

    while True:

        text = input("\nEnter expression (or exit): ")

        if text.lower() == "exit":
            break

        try:

            tokens = lexer.tokenize(text)

            print("\nTOKENS")

            for t in tokens:
                print(t)

            parser = Parser(tokens)

            ast = parser.parse()

            print("\nAST STRUCTURE")

            print_ast(ast)

        except Exception as e:

            print("Error:", e)