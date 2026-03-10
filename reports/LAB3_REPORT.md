# Laboratory Work #3: Lexer & Scanner Implementation

**Course:** Formal Languages & Finite Automata  
**Author:** Daria Tureac  


---

## Theory

Lexical analysis is the first stage in the processing of source code in compilers and interpreters.  
Its purpose is to transform a sequence of characters into a sequence of **tokens** that represent meaningful elements of a language.

A **lexer** (also called a *tokenizer* or *scanner*) reads an input string and divides it into **lexemes**, which are then categorized into **tokens**.

The difference between **lexemes** and **tokens** is important:

* **Lexeme** – the actual substring extracted from the input (e.g., `"10.5"`).
* **Token** – the classification or type assigned to that lexeme (e.g., `FLOAT`).
---

## Objectives:
1. Understand the concept of **lexical analysis**.
2. Learn how a **lexer/tokenizer** works internally.
3. Implement a **custom lexer in Python** capable of recognizing multiple token types.
4. Demonstrate the lexer functionality using interactive input.
---

## Implementation description

The lexer was implemented in **Python** using the `re` module for **regular expressions**.

The program reads an input expression and splits it into tokens according to predefined patterns.

### Token Specification

The lexer identifies several categories of tokens:

| Token Type | Description |
|------------|-------------|
| SCI_NUMBER | Scientific notation numbers (e.g., `1.2e-5`) |
| FLOAT | Floating-point numbers |
| INTEGER | Integer numbers |
| FUNCTION | Trigonometric functions (`sin`, `cos`, `tan`) |
| IDENT | Variable names |
| ASSIGN | Assignment operator (`=`) |
| PLUS / MINUS | Arithmetic operators |
| MUL / DIV | Multiplication and division |
| LPAREN / RPAREN | Parentheses |
| WS | Whitespace (ignored) |
| MISMATCH | Invalid characters |

The order of token rules is important because **more specific patterns must be evaluated first**.

---

## Code snippets

**Token Specification**

The lexer defines token patterns using regular expressions.
```python
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

```
Each token type is associated with a regular expression used to recognize lexemes in the input string.

**Tokenization Process**

The lexer scans the input string and generates tokens.
```python
       def tokenize(self, code):
    tokens = []
    for match in re.finditer(self.regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == 'WS':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character: "{value}"')
        else:
            tokens.append({'type': kind, 'value': value})

    return tokens
```

Logic of the algorithm:

1. The program scans the input string using re.finditer.

2. Each match corresponds to a token type.

3. Whitespace tokens are ignored.

4. Invalid characters produce an error.

5. Valid tokens are added to the token list.

**Interactive Lexer**

The program allows the user to input expressions interactively.

```python
        while True:
    user_input = input("Enter expression > ")

    if user_input.lower() == 'exit':
        break

    token_stream = lexer.tokenize(user_input)

    for token in token_stream:
        print(token)
```

## Conclusions/Screenshots/Results

**Example Input:**
```python
sin(10.5) + 3 * 2e3
```
**Console Output:**



```python
TOKEN TYPE      | VALUE
------------------------------
FUNCTION        | sin
LPAREN          | (
FLOAT           | 10.5
RPAREN          | )
PLUS            | +
INTEGER         | 3
MUL             | *
SCI_NUMBER      | 2e3
```

## Challenges & Difficulties

1. **Token Priority**

     Regular expressions must be defined in the correct order.
Specific tokens such as scientific numbers must appear before general tokens like integers.


2. **Handling Invalid Characters**

   A special rule MISMATCH was implemented to detect unexpected characters and raise a syntax error.


3. **Supporting Multiple Number Formats**

   The lexer was designed to recognize integers, floating-point numbers, and scientific notation, which required multiple regex patterns.

## Conclusions

This laboratory work demonstrated the process of lexical analysis and the implementation of a simple lexer using Python.

The lexer successfully converts input expressions into structured tokens using regular expressions.
It supports various token types including numbers, identifiers, operators, parentheses, and trigonometric functions.

The experiment illustrates how lexical analysis transforms raw text into a structured token stream, simplifying the next stages of language processing.
## References
[1] https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html

[2] https://en.wikipedia.org/wiki/Lexical_analysis

Course materials: Formal Languages & Finite Automata – Cretu Dumitru