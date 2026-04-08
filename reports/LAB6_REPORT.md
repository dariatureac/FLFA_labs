# Laboratory Work #6: Parser & Building an Abstract Syntax Tree

**Course:** Formal Languages & Finite Automata  
**Author:** Daria Tureac

---

## Theory

Parsing is the process of analyzing a sequence of tokens to determine its grammatical structure according to a given formal grammar.

In compiler design, parsing is used after lexical analysis in order to extract the syntactic structure of a program.

A parser produces a data structure called a **Parse Tree** or **Abstract Syntax Tree (AST)**.

An **Abstract Syntax Tree (AST)** is a hierarchical tree representation of the structure of source code. Each node represents a language construct such as:

- operators
- numbers
- variables
- function calls

Unlike parse trees, ASTs remove unnecessary syntactic elements and represent only the essential structure of the program.

---

## Objectives:
1. Understand the concept of parsing.
2. Implement token classification using TokenType.
3. Build data structures representing an Abstract Syntax Tree.
4. Implement a parser that constructs the AST from tokens.
---

# Implementation description and Code Snippets

The implementation consists of four main components:

• TokenType  
• Lexer  
• Parser  
• AST Nodes

## TokenType

TokenType is implemented as an Enum and represents all possible token categories.

Examples:

```python
from enum import Enum

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
```
Using an enum improves code readability and simplifies token comparison during parsing.

---

## Lexer

The lexer performs **lexical analysis** using regular expressions.

Each token type is associated with a specific regex pattern.

```python
self.token_specification = [
    ('SCI_NUMBER', r'\d+(\.\d+)?[eE][+-]?\d+'),
    ('FLOAT', r'\d+\.\d+'),
    ('INTEGER', r'\d+'),
    ('FUNCTION', r'sin|cos|tan'),
    ('IDENT', r'[a-zA-Z_]\w*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
]
```
```python
def tokenize(self, code):
    tokens = []

    for match in re.finditer(self.regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "WS":
            continue

        elif kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character {value}")

        else:
            tokens.append({
                "type": TokenType[kind],
                "value": value
            })

    return tokens
```

The lexer scans the input text and converts it into a stream of tokens.

Example input:


3 + 4 * 5


Generated tokens:


```python
INTEGER 3
PLUS +
INTEGER 4
MUL *
INTEGER 5
```

---

## Abstract Syntax Tree

The AST is composed of different node types:

• NumberNode  
• VariableNode  
• BinaryOpNode  
• FunctionNode  

Each node represents a specific construct in the expression.

```python
class BinaryOpNode(ASTNode):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class NumberNode(ASTNode):

    def __init__(self, value):
        self.value = value
```
Example structure:


```python
Operator(+)
Number(3)
Operator(*)
Number(4)
Number(5)
```

This tree reflects operator precedence.

---

## Parser

The parser performs **syntactic analysis**.

The grammar used is:


expression → term ((+ | -) term)*

term → factor ((* | /) factor)*

factor → number | variable | function | (expression)

```python
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
```

The parser processes tokens sequentially and constructs AST nodes.

Operator precedence is handled through the grammar hierarchy:

expression → addition/subtraction  
term → multiplication/division  
factor → basic elements

---

## Results

Example input:


```3 + 4 * 5```


Generated AST:


```python
Operator(+)
Number(3)
Operator(*)
Number(4)
Number(5)
```

Example with function:


```sin(3+4)```


AST:


```python
Function(sin)
Operator(+)
Number(3)
Number(4)
```

---

# Challenges

One challenge was implementing operator precedence correctly.

Another challenge involved managing the parser pointer while navigating the token stream.

Additionally, creating a clear AST structure required designing several node classes.

---

# Conclusions

This laboratory work demonstrates how lexical analysis and parsing work together to analyze program structure.

By implementing an AST builder, we created a structured representation of mathematical expressions that can later be used for interpretation, compilation, or optimization.

The project highlights the relationship between formal grammars, parsing algorithms, and data structures used in compilers.

---

# References

https://en.wikipedia.org/wiki/Parsing  

https://en.wikipedia.org/wiki/Abstract_syntax_tree