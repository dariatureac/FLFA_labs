import re

class Lexer:
    def __init__(self):
        # The order is critical: most specific patterns must come first
        self.token_specification = [
            # Scientific notation (e.g., 1.2e-5, 5E10)
            ('SCI_NUMBER', r'\d+(\.\d+)?[eE][+-]?\d+'),
            # Floating-point numbers (e.g., 10.5)
            ('FLOAT',      r'\d+\.\d+'),
            # Integer numbers
            ('INTEGER',    r'\d+'),
            # Trigonometric functions
            ('FUNCTION',   r'sin|cos|tan'),
            # Assignment operator
            ('ASSIGN',     r'='),
            # Identifiers / Variables
            ('IDENT',      r'[a-zA-Z_]\w*'),
            # Arithmetic operators
            ('PLUS',       r'\+'),
            ('MINUS',      r'-'),
            ('MUL',        r'\*'),
            ('DIV',        r'/'),
            # Parentheses
            ('LPAREN',     r'\('),
            ('RPAREN',     r'\)'),
            # Whitespace (to be ignored)
            ('WS',         r'\s+'),
            # Any other character (error)
            ('MISMATCH',   r'.'),
        ]
        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification)

    def tokenize(self, code):
        tokens = []
        for match in re.finditer(self.regex, code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'WS':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected character: "{value}" at position {match.start()}')
            else:
                tokens.append({'type': kind, 'value': value})
        return tokens

if __name__ == "__main__":
    lexer = Lexer()
    print("=== Advanced Interactive Lexer (type 'exit' to quit) ===")
    while True:
        user_input = input("\nEnter expression > ")
        if user_input.lower() == 'exit':
            break
        try:
            token_stream = lexer.tokenize(user_input)
            print(f"\n{'TOKEN TYPE':<15} | {'VALUE'}")
            print("-" * 30)
            for token in token_stream:
                print(f"{token['type']:<15} | {token['value']}")
        except SyntaxError as e:
            print(f"Error: {e}")